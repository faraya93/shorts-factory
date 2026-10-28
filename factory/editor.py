"""Editor (Fase B): monta el video final de una producción. 100% local, no usa fal.ai.

Uso: python factory/editor.py productions/<canal>/<video>
"""

import argparse
import asyncio
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path

import edge_tts
from PIL import Image, ImageDraw, ImageFont

import overlays
import visual_identity as vid
from overlays import (find_word_start, norm_word, render_end_card, render_overlay, start_offset, track_expr, validate_end_card,
                      validate_scene_overlays, visible_seconds)

def overlays_fonts() -> dict:
    import overlays
    return overlays.FONTS


DEFAULT_VOICE = "es-CL-LorenzoNeural"
AUDIO_DEFAULTS = {"narration_volume": 1.0, "effects_volume": 0.30, "music_volume": 0.10,
                  "clip_audio": "off", "clip_gate_db": -35.0, "music_file": None, "music_credit": None}
AUDITION_VOICES =["es-CL-LorenzoNeural", "es-MX-JorgeNeural", "es-ES-AlvaroNeural", "es-CL-CatalinaNeural"]
W, H, FPS = 1080, 1920, 30
MAX_SLOWDOWN = 1.25

# Subtitles (reference style, owner 2026-10-26): fixed UPPER band, whole phrase visible, the spoken word bold white and the
# others grey (~55%); key words listed in the scene's `subtitle_emphasis` get a thin teal selection box while they are spoken.
FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
SUB_FONT_SIZE = 57          # px
SUB_STROKE = 4              # px, thin black outline (readability over bright parts of the scene)
SUBTITLE_Y_CENTER = 0.24    # channel constant (moves to channels/umbrella-es.yaml in Task F): block center, fraction of frame height
SUB_MAX_WIDTH = 940         # px, maximum line width before wrapping
SUB_CENTER_Y = round(H * SUBTITLE_Y_CENTER)
SUB_WORD_COLOR = (150, 150, 155)       # not-current words: grey (~55% white)
SUB_CURRENT_COLOR = (255, 255, 255)    # current word: bold white
SUB_EMPH_COLOR = (103, 205, 190)       # selection box of an emphasised word (annotation teal)
SUB_BOX_PAD_X, SUB_BOX_PAD_Y, SUB_BOX_RADIUS = 12, 6, 12
SUB_BOX_WIDTH, SUB_HANDLE = 3, 7       # selection box line width; corner handle half-size
CUE_MAX_WORDS, CUE_MAX_CHARS = 4, 26


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"\nERROR: falló {cmd[0]} (código {r.returncode})\n$ {' '.join(cmd)}\n{r.stderr[-3000:]}")
        sys.exit(1)
    return r


def probe(path: Path) -> dict:
    out = run(["ffprobe", "-v", "error", "-show_entries",
               "stream=codec_type,width,height:format=duration", "-of", "json", str(path)]).stdout
    info = json.loads(out)
    return {"duration": float(info["format"]["duration"]),
            "has_audio": any(s["codec_type"] == "audio" for s in info["streams"])}


def gate_clip(path: Path, gate_db: float) -> dict:
    """No-music validator: a clip whose audio is louder (mean volume) than gate_db is music-level
    continuous audio and is muted entirely; at or below it, it is genuine foley and is admitted."""
    if not probe(path)["has_audio"]:
        return {"mean_db": None, "admitted": False, "decision": "no audio track"}
    r = run(["ffmpeg", "-nostats", "-v", "info", "-i", str(path), "-vn", "-af", "volumedetect", "-f", "null", "-"])
    m = re.search(r"mean_volume:\s*(-?[\d.]+|-inf) dB", r.stderr)
    if not m:
        print(f"ERROR: volumedetect gave no mean_volume for {path}")
        sys.exit(1)
    mean_db = float(m.group(1))
    admitted = mean_db <= gate_db
    return {"mean_db": mean_db, "admitted": admitted, "decision": "ADMITTED" if admitted else "MUTED"}


def print_gate_table(rows: list[tuple[str, dict]], gate_db: float) -> None:
    print(f"clip audio gate: mean volume > {gate_db:g} dB is muted, <= {gate_db:g} dB is admitted")
    print(f"{'scene':<10}{'mean dB':>9}  decision")
    for name, g in rows:
        mean = f"{g['mean_db']:.1f}" if g["mean_db"] is not None else "n/a"
        print(f"{name:<10}{mean:>9}  {g['decision']}")


# --- Narración (edge-tts) ---------------------------------------------------------------

def srt_time(sec: float) -> str:
    ms = round(sec * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def group_cues(tokens: list[str], events: list[dict]) -> list[dict]:
    """Group words into short phrases (max CUE_MAX_WORDS words). Events carry timings but no punctuation,
    so they are aligned 1:1 with the words of the original text. Each cue keeps its per-word timings."""
    if len(tokens) != len(events):
        sys.exit(f"ERROR: edge-tts returned {len(events)} words and the text has {len(tokens)}; "
                 "the subtitles cannot be aligned.")
    cues, cur = [], []

    def flush():
        if cur:
            cues.append({"start": cur[0]["start"], "end": cur[-1]["end"], "words": list(cur)})
            cur.clear()

    for tok, ev in zip(tokens, events):
        word = {"text": tok, "start": ev["offset"] / 1e7, "end": (ev["offset"] + ev["duration"]) / 1e7}
        if cur and (len(cur) >= CUE_MAX_WORDS or len(" ".join(w["text"] for w in cur) + " " + tok) > CUE_MAX_CHARS):
            flush()
        cur.append(word)
        text = " ".join(w["text"] for w in cur)
        if re.search(r"[.?!:;]$", tok) or (tok.endswith(",") and len(text) >= 10):
            flush()
    flush()
    # no gaps between close phrases: a cue lasts until the next one starts
    for i, cue in enumerate(cues[:-1]):
        if cues[i + 1]["start"] - cue["end"] < 0.5:
            cue["end"] = cues[i + 1]["start"]
    return cues


async def synthesize(text: str, voice: str, mp3: Path, srt: Path | None = None) -> None:
    comm = edge_tts.Communicate(text, voice, boundary="WordBoundary")
    audio, events = bytearray(), []
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            audio += chunk["data"]
        elif chunk["type"] == "WordBoundary":
            events.append(chunk)
    mp3.write_bytes(audio)
    if srt is None:  # audition mode: audio only
        return
    cues = group_cues(text.split(), events)
    srt.write_text("".join(f"{i}\n{srt_time(c['start'])} --> {srt_time(c['end'])}\n"
                           f"{' '.join(w['text'] for w in c['words'])}\n\n"
                           for i, c in enumerate(cues, 1)), encoding="utf-8")
    words_json(srt).write_text(json.dumps(cues, ensure_ascii=False, indent=1), encoding="utf-8")


def words_json(srt: Path) -> Path:
    """Per-word timings of a scene's phrases, next to its SRT (scene-NN.srt -> scene-NN.words.json)."""
    return srt.with_suffix(".words.json")


# --- Subtítulos como PNG (este ffmpeg no trae libass/freetype) -------------------------

def layout_cue(texts: list[str], font: ImageFont.FreeTypeFont) -> dict:
    """Wrap a phrase into centred lines once, so every highlight state of the phrase shares one layout."""
    d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    space = d.textlength(" ", font=font)
    widths = [d.textlength(w, font=font) for w in texts]
    lines, cur, cur_w = [], [], 0.0
    for i, w in enumerate(widths):
        if cur and cur_w + space + w > SUB_MAX_WIDTH:
            lines.append((cur, cur_w))
            cur, cur_w = [], 0.0
        cur_w += (space if cur else 0) + w
        cur.append(i)
    lines.append((cur, cur_w))
    ascent, descent = font.getmetrics()
    line_h, gap = ascent + descent, 14
    pad_x, pad_y = SUB_BOX_PAD_X + SUB_STROKE, SUB_BOX_PAD_Y + SUB_STROKE
    return {"lines": lines, "widths": widths, "space": space, "line_h": line_h, "gap": gap,
            "pad_x": pad_x, "pad_y": pad_y,
            "w": math.ceil(max(lw for _, lw in lines)) + 2 * pad_x,
            "h": len(lines) * line_h + (len(lines) - 1) * gap + 2 * pad_y}


def render_cue_state(texts: list[str], current: int, lay: dict, path: Path, font: ImageFont.FreeTypeFont,
                     font_reg: ImageFont.FreeTypeFont | None = None, emphasis: list[bool] | None = None) -> None:
    """One PNG of the phrase with word `current` marked: bold white; the others grey (regular weight, centred in the same slot);
    an emphasised current word also gets a thin teal selection box with corner handles."""
    img = Image.new("RGBA", (lay["w"], lay["h"]), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    reg = font_reg or font
    y = lay["pad_y"]
    for idxs, line_w in lay["lines"]:
        x = (lay["w"] - line_w) / 2
        for i in idxs:
            slot_w = lay["widths"][i]
            if i == current:
                draw.text((x, y), texts[i], font=font, fill=SUB_CURRENT_COLOR, stroke_width=SUB_STROKE, stroke_fill="black")
                if emphasis and emphasis[i]:
                    x0, y0, x1, y1 = x - SUB_BOX_PAD_X, y - SUB_BOX_PAD_Y, x + slot_w + SUB_BOX_PAD_X, y + lay["line_h"] + SUB_BOX_PAD_Y
                    draw.rounded_rectangle([x0, y0, x1, y1], radius=SUB_BOX_RADIUS, outline=SUB_EMPH_COLOR, width=SUB_BOX_WIDTH)
                    for hx, hy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
                        draw.rectangle([hx - SUB_HANDLE, hy - SUB_HANDLE, hx + SUB_HANDLE, hy + SUB_HANDLE], fill=SUB_EMPH_COLOR)
            else:
                tw = draw.textlength(texts[i], font=reg)
                draw.text((x + (slot_w - tw) / 2, y), texts[i], font=reg, fill=SUB_WORD_COLOR, stroke_width=SUB_STROKE,
                          stroke_fill="black")
            x += slot_w + lay["space"]
        y += lay["line_h"] + lay["gap"]
    img.save(path)


# --- Montaje ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("production", type=Path)
    ap.add_argument("--voice", help="edge-tts voice; default: scenes.json 'voice', else " + DEFAULT_VOICE)
    ap.add_argument("--audition", action="store_true",
                    help="render scene 1's narration with each AUDITION_VOICES into audio/audition/ and exit")
    ap.add_argument("--gate-report", action="store_true",
                    help="measure each clip's audio against audio.clip_gate_db, print the table and exit (no render)")
    ap.add_argument("--only-scene", type=int, metavar="N",
                    help="test render of scene N only, written to build/test-scene-NN.mp4 (final.mp4 is not touched)")
    args = ap.parse_args()
    prod = args.production
    cfg = json.loads((prod / "scenes.json").read_text())
    voice = args.voice or cfg.get("voice") or DEFAULT_VOICE

    if args.audition:
        out_dir = prod / "audio" / "audition"
        out_dir.mkdir(parents=True, exist_ok=True)
        text = cfg["scenes"][0]["narration"]
        for v in AUDITION_VOICES:
            path = out_dir / f"scene-01-{v}.mp3"
            asyncio.run(synthesize(text, v, path))
            print(f"{v:<24}{probe(path)['duration']:>6.2f} s  {path.resolve()}")
        return 0

    if args.gate_report:
        gate_db = {**AUDIO_DEFAULTS, **cfg.get("audio", {})}["clip_gate_db"]
        rows = []
        for s in cfg["scenes"]:
            clip = prod / "clips" / f"scene-{s['id']:02d}.mp4"
            if not clip.exists():
                print(f"ERROR: missing clip {clip}")
                return 1
            rows.append((f"scene-{s['id']:02d}", gate_clip(clip, gate_db)))
        print_gate_table(rows, gate_db)
        return 0

    scenes = cfg["scenes"]
    if args.only_scene is not None:
        scenes = [s for s in scenes if s["id"] == args.only_scene]
        if not scenes:
            print(f"ERROR: no scene with id {args.only_scene}")
            return 1
    clips, audio_dir, build = prod / "clips", prod / "audio", prod / "build"
    identity = cfg.get("visual_identity")
    problems = vid.validate(identity) if identity else []
    for s in scenes:
        problems += validate_scene_overlays(s["id"], s["data_overlays"]) if "data_overlays" in s else []
    end_card = cfg.get("end_card") if args.only_scene is None else None     # test renders of one scene have no end card
    problems += validate_end_card(cfg.get("end_card"))
    if problems:
        print("ERROR: invalid scenes.json:\n" + "\n".join(f"  - {x}" for x in problems))
        return 1
    audio_dir.mkdir(exist_ok=True)
    build.mkdir(exist_ok=True)

    # 1. Todos los clips deben existir
    missing = [f"scene-{s['id']:02d}.mp4" for s in scenes if not (clips / f"scene-{s['id']:02d}.mp4").exists()]
    if missing:
        print(f"ERROR: faltan clips en {clips}: {', '.join(missing)}. Corre factory/producer.py primero.")
        return 1

    # 2. Narración por escena (se reutiliza si el texto y la voz no cambiaron)
    meta_path = audio_dir / "audio.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    for s in scenes:
        n = f"scene-{s['id']:02d}"
        digest = hashlib.sha256(f"{voice}|{s['narration']}".encode()).hexdigest()
        if (meta.get(n) == digest and (audio_dir / f"{n}.mp3").exists() and (audio_dir / f"{n}.srt").exists()
                and words_json(audio_dir / f"{n}.srt").exists()):
            print(f"narración {n}: reutilizada")
            continue
        print(f"narración {n}: generando con {voice}")
        asyncio.run(synthesize(s["narration"], voice, audio_dir / f"{n}.mp3", audio_dir / f"{n}.srt"))
        meta[n] = digest
        meta_path.write_text(json.dumps(meta, indent=2))

    # 3. Slots y ajuste de cada clip
    plan, report = [], []
    for s in scenes:
        n = f"scene-{s['id']:02d}"
        narr = probe(audio_dir / f"{n}.mp3")["duration"]
        info = probe(clips / f"{n}.mp4")
        slot_frames = math.ceil(narr * FPS - 1e-6)
        slot, d = slot_frames / FPS, info["duration"]
        factor, freeze = 1.0, 0.0
        if d >= slot:
            note = f"recortado {d - slot:.2f} s" if d > slot else "sin ajuste"
        else:
            factor = min(slot / d, MAX_SLOWDOWN)
            freeze = max(0.0, slot - d * factor)
            note = f"ralentizado x{factor:.3f}" + (f" + último frame congelado {freeze:.2f} s" if freeze > 0.001 else "")
        gate = gate_clip(clips / f"{n}.mp4", {**AUDIO_DEFAULTS, **cfg.get("audio", {})}["clip_gate_db"])
        plan.append({"s": s, "n": n, "dur": d, "slot": slot, "slot_frames": slot_frames, "factor": factor, "freeze": freeze,
                     "has_audio": info["has_audio"], "gate": gate})
        report.append((s["id"], s["name"], narr, slot, d, info["has_audio"], note))

    # 4. Subtítulos globales (cues por escena desplazadas por los slots acumulados) -> PNGs
    font_path = next((f for f in [overlays.MONTSERRAT, *FONT_CANDIDATES] if Path(f).exists()), None)
    if not font_path:
        print("ERROR: no encontré una fuente en negrita en FONT_CANDIDATES.")
        return 1
    font = overlays.font("bold", SUB_FONT_SIZE)          # Montserrat ExtraBold (factory/assets/fonts)
    font_reg = overlays.font("regular", SUB_FONT_SIZE)   # Montserrat SemiBold
    for old in build.glob("cue-*.png"):
        old.unlink()
    # one PNG per highlight state: for each phrase, one image per word with that word marked
    for old in (build / "ov").glob("*.png") if (build / "ov").exists() else []:
        old.unlink()
    cue_imgs, srt_cues, offset, n_phrases, ov_list = [], [], 0.0, 0, []
    for p in plan:
        slot_end = offset + p["slot"]
        cues = json.loads(words_json(audio_dir / f"{p['n']}.srt").read_text(encoding="utf-8"))
        scene_words = [w for c in cues for w in c["words"]]                    # {text, start, end} from the scene's narration start
        emph_set = {norm_word(x) for x in p["s"].get("subtitle_emphasis", [])}
        for cue in cues:
            texts = [w["text"] for w in cue["words"]]
            emphasis = [norm_word(t) in emph_set for t in texts]
            lay = layout_cue(texts, font)
            srt_cues.append((offset + cue["start"], min(offset + cue["end"], slot_end), " ".join(texts)))
            n_phrases += 1
            for k, word in enumerate(cue["words"]):
                a = offset + (cue["start"] if k == 0 else word["start"])
                b = offset + (cue["words"][k + 1]["start"] if k + 1 < len(texts) else cue["end"])
                png = build / f"cue-{len(cue_imgs):03d}.png"
                render_cue_state(texts, k, lay, png, font, font_reg, emphasis)
                cue_imgs.append((png, lay["w"], lay["h"], a, min(b, slot_end)))
        for spec in p["s"].get("data_overlays", []):  # timed from this scene's narration start (or locked to a spoken word)
            try:
                start = offset + start_offset(spec, scene_words)
            except ValueError as e:
                print(f"ERROR: scene {p['s']['id']}: {e}")
                return 1
            meta_ov = render_overlay(spec, build / "ov", f"ov{len(ov_list):02d}", font_path, FPS)
            ov_list.append({**meta_ov, "start": start, "end": min(start + visible_seconds(spec), slot_end),
                            "type": spec["type"], "scene": p["n"], "word": spec.get("at_word")})
        offset += p["slot"]
    total = offset
    ext = float(end_card.get("duration_s", 4.0)) if end_card else 0.0       # the end card extends the video past the narration
    end_meta = render_end_card(end_card, build / "ov", "endcard", FPS) if end_card else None
    (build if args.only_scene is not None else prod).joinpath("final.srt").write_text(
        "".join(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{t}\n\n" for i, (a, b, t) in enumerate(srt_cues, 1)),
        encoding="utf-8")

    # 4a. Visual QA: sampled background colour of each raw clip vs the identity spec (flags, never blocks)
    qa_rows = []
    if identity:
        for p in plan:
            applies = vid.qa_applies(cfg.get("primary_engine"), p["s"])
            result = vid.qa_clip(clips / f"{p['n']}.mp4", identity, build / "qa", p["dur"]) if applies else None
            qa_rows.append({"scene": p["n"], "shot_type": p["s"].get("shot_type", "establishing"),
                            **(result or {}), "status": vid.qa_status(applies, result, p["s"].get("qa_note"))})
        (build / "visual-qa.json").write_text(json.dumps(qa_rows, indent=2) + "\n")

    # 4b. Audio profile: scenes.json declares the recipe, the code only provides the capability
    audio = {**AUDIO_DEFAULTS, **cfg.get("audio", {})}
    if audio["clip_audio"] not in ("off", "effects"):
        print(f"ERROR: audio.clip_audio must be 'off' or 'effects', got {audio['clip_audio']!r}")
        return 1
    fx = audio["clip_audio"] == "effects"
    music_path, music_note = None, "SKIPPED (no music_file configured)"
    if audio["music_file"]:
        candidate = prod / audio["music_file"]
        if candidate.is_file():
            music_path = candidate
            src = probe(candidate)["duration"]
            music_note = (f"ACTIVE x{audio['music_volume']:.2f} ({candidate.name}, {src:.1f} s source, "
                          f"{'looped' if src < total else 'trimmed'} to {total:.1f} s)")
        else:
            music_note = f"SKIPPED ({audio['music_file']} not found in {prod})"

    # 5. filter_complex: conformar clips + audio + concat + subtítulos, una sola codificación
    n_sc = len(plan)
    unify = vid.unify_filter(identity)
    parts = []
    for i, p in enumerate(plan):
        chain = [f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos", f"crop={W}:{H}",
                 "setsar=1", f"fps={FPS}"]
        if p["factor"] != 1.0:
            chain += [f"setpts=PTS*{p['factor']:.6f}", f"fps={FPS}"]
        if p["freeze"] > 0.001:
            chain.append(f"tpad=stop_mode=clone:stop_duration={p['freeze'] + 0.2:.3f}")
        chain += [f"trim=end_frame={p['slot_frames']}", "setpts=PTS-STARTPTS"]
        if unify:  # ONE shared pass for every scene, whatever its engine: grade + grain + vignette
            chain.append(unify)
        parts.append(f"[{i}:v]{','.join(chain)}[v{i}]")
        parts.append(f"[{n_sc + i}:a]aresample=48000,aformat=channel_layouts=stereo,"
                     f"apad=whole_dur={p['slot']:.5f},atrim=duration={p['slot']:.5f},asetpts=PTS-STARTPTS[a{i}]")
        if fx:  # the clip's own audio, conformed exactly like its video (slow down / silence pad / trim)
            if p["has_audio"] and p["gate"]["admitted"]:  # muted clips (music-level audio) become silence
                tempo = f"atempo={1 / p['factor']:.6f}," if p["factor"] != 1.0 else ""
                parts.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,{tempo}"
                             f"apad=whole_dur={p['slot']:.5f},atrim=duration={p['slot']:.5f},asetpts=PTS-STARTPTS[f{i}]")
            else:
                parts.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={p['slot']:.5f},asetpts=PTS-STARTPTS[f{i}]")
    if fx:
        parts.append("".join(f"[v{i}][a{i}][f{i}]" for i in range(n_sc)) + f"concat=n={n_sc}:v=1:a=2[vcat][acat][fcat]")
    else:
        parts.append("".join(f"[v{i}][a{i}]" for i in range(n_sc)) + f"concat=n={n_sc}:v=1:a=1[vcat][acat]")
    last = "vcat"
    if ext:
        parts.append(f"[vcat]tpad=stop_mode=clone:stop_duration={ext:.3f}[vend]")
        last = "vend"
    for k, (png, w, h, a, b) in enumerate(cue_imgs):
        x, y = (W - w) // 2, SUB_CENTER_Y - h // 2
        parts.append(f"[{last}][{2 * n_sc + k}:v]overlay=x={x}:y={y}:enable='gte(t,{a:.3f})*lt(t,{b:.3f})'[o{k}]")
        last = f"o{k}"
    ov_base = 2 * n_sc + len(cue_imgs)
    for k, ov in enumerate(ov_list):  # data overlays: frame centre; sequence delayed to its start, last frame held
        parts.append(f"[{ov_base + k}:v]setpts=PTS+{ov['start']:.3f}/TB[ovs{k}]")
        if "track" in ov:       # keyframed: piecewise-linear position over absolute time
            ox = track_expr([(t, x) for t, x, y in ov["track"]], ov["start"])
            oy = track_expr([(t, y) for t, x, y in ov["track"]], ov["start"])
            pos = f"x='{ox}':y='{oy}'"
        elif "left" in ov:
            pos = f"x={ov['left']}:y={ov['top']}"
        else:
            pos = f"x={(W - ov['w']) // 2}:y={(H - ov['h']) // 2}"
        parts.append(f"[{last}][ovs{k}]overlay={pos}:enable='gte(t,{ov['start']:.3f})*lt(t,{ov['end']:.3f})'[p{k}]")
        last = f"p{k}"
    if end_meta:                # dim the final frame and fade in the placeholder logo + handle
        k_end = ov_base + len(ov_list)
        parts.append(f"[{k_end}:v]setpts=PTS+{total:.3f}/TB[ovend]")
        parts.append(f"[{last}][ovend]overlay=x=0:y=0:enable='gte(t,{total:.3f})'[pend]")
        last = "pend"

    if ext:                      # narration/effects are silent over the end card; the music keeps going
        parts.append(f"[acat]apad=whole_dur={total + ext:.5f}[acat2]")
        acat_label = "acat2"
        if fx:
            parts.append(f"[fcat]apad=whole_dur={total + ext:.5f}[fcat2]")
    else:
        acat_label = "acat"
    # audio mix: normalize=0 keeps every layer at exactly its configured volume; the limiter only prevents clipping
    parts.append(f"[{acat_label}]volume={audio['narration_volume']}[nar]")
    layers = ["[nar]"]
    if fx:
        parts.append(f"[{'fcat2' if ext else 'fcat'}]volume={audio['effects_volume']}[fxv]")
        layers.append("[fxv]")
    if music_path:
        music_idx = ov_base + len(ov_list) + (1 if end_meta else 0)
        parts.append(f"[{music_idx}:a]aresample=48000,aformat=channel_layouts=stereo,"
                     f"atrim=duration={total + ext:.5f},asetpts=PTS-STARTPTS,volume={audio['music_volume']}[mus]")
        layers.append("[mus]")
    if len(layers) > 1:
        parts.append("".join(layers) + f"amix=inputs={len(layers)}:duration=first:normalize=0,"
                     "alimiter=limit=0.95:level=0[aout]")
        audio_out = "[aout]"
    else:
        audio_out = "[nar]"
    script = build / "filter.txt"
    script.write_text(";\n".join(parts))

    cmd = ["ffmpeg", "-y", "-v", "error", "-stats"]
    for p in plan:
        cmd += ["-i", str(clips / f"{p['n']}.mp4")]       # clip audio only enters the mix when clip_audio == "effects"
    for p in plan:
        cmd += ["-i", str(audio_dir / f"{p['n']}.mp3")]
    for png, *_ in cue_imgs:
        cmd += ["-i", str(png)]
    for ov in ov_list:
        cmd += ["-framerate", str(FPS), "-i", ov["pattern"]]
    if end_meta:
        cmd += ["-framerate", str(FPS), "-i", end_meta["pattern"]]
    if music_path:
        cmd += ["-stream_loop", "-1", "-i", str(music_path)]
    final = build / f"test-scene-{args.only_scene:02d}.mp4" if args.only_scene is not None else prod / "final.mp4"
    cmd += ["-/filter_complex", str(script), "-map", f"[{last}]", "-map", audio_out,
            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-t", f"{total + ext:.5f}", str(final)]
    print(f"\nCodificando {len(cue_imgs)} estados de subtítulo sobre {total:.1f} s de video ...")
    run(cmd)

    # 6. Cover: scene 1 at ~1 s, clean (no subtitles); not for test renders
    if args.only_scene is None:
        run(["ffmpeg", "-y", "-v", "error", "-ss", "1", "-i", str(clips / "scene-01.mp4"), "-frames:v", "1",
             "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}",
             "-q:v", "2", str(prod / "cover.jpg")])

    # 7. Resumen
    out = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate,pix_fmt,codec_name:format=duration",
                          "-of", "json", str(final)]).stdout)
    v = out["streams"][0]
    print(f"\n{'esc':<4}{'nombre':<15}{'narración':>10}{'slot':>8}{'clip':>8}  clip audio       ajuste")
    for (sid, name, narr, slot, d, has_audio, note), p in zip(report, plan):
        if not has_audio:
            clip_audio = "no"
        elif not fx:
            clip_audio = "yes (discarded)"
        else:
            clip_audio = "yes (admitted)" if p["gate"]["admitted"] else "yes (muted)"
        print(f"{sid:<4}{name:<15}{narr:>9.2f}s{slot:>7.2f}s{d:>7.2f}s  {clip_audio:<16}{note}")
    gate_db = audio["clip_gate_db"]
    print()
    print_gate_table([(p["n"], p["gate"]) for p in plan], gate_db)
    if not fx:
        print("(clip_audio is 'off': decisions are logged but no clip audio is mixed)")
    (build / "audio-gate.json").write_text(json.dumps(
        {"clip_gate_db": gate_db, "clip_audio": audio["clip_audio"],
         "decisions": [{"scene": p["n"], **p["gate"]} for p in plan]}, indent=2) + "\n")
    print(f"\nDuración total: {float(out['format']['duration']):.2f} s (timeline {total:.2f} s"
          + (f" + end card {ext:.1f} s)" if ext else ")"))
    print(f"Video: {v['width']}x{v['height']} @ {v['r_frame_rate']} fps, {v['codec_name']} {v['pix_fmt']}")
    print(f"Voz: {voice}")
    print("Audio profile: "
          f"narration x{audio['narration_volume']:.2f} | "
          f"effects {'ACTIVE x%.2f, gate %g dB' % (audio['effects_volume'], audio['clip_gate_db']) if fx else 'OFF (clip audio discarded)'} | "
          f"music {music_note}")
    if music_path and audio.get("music_credit"):
        print(f"Music credit: {audio['music_credit']}")
    print(f"Shared unify pass: {unify or 'none (no visual_identity)'}")
    if qa_rows:
        tol = identity.get("qa_tolerance_de", vid.DEFAULT_TOLERANCE_DE)
        print(f"Background QA vs {identity['background']['hex']} (CIE76 dE <= {tol:g}; establishing shots and code3d "
              "only; marks are review signals, not defects):")
        for r in qa_rows:
            sampled = f"sampled {r['hex']}  dE {r['delta_e']:>5}" if "hex" in r else "not sampled"
            print(f"  {r['scene']}: {sampled}  {r['status']}")
    for ov in ov_list:
        locked = f" @word {ov['word']!r}" if ov.get("word") else ""
        print(f"Data overlay: {ov['scene']} {ov['type']} {ov['start']:.2f}-{ov['end']:.2f} s ({ov['frames']} frames){locked}")
    print(f"Subtítulos: {n_phrases} frases / {len(cue_imgs)} estados de palabra | fuente {Path(font_path).name} {SUB_FONT_SIZE}px, contorno {SUB_STROKE}px")
    print(f"{final.name}: {final.stat().st_size / 1e6:.1f} MB" +
          ("" if args.only_scene is not None else f" | cover.jpg: {(prod / 'cover.jpg').stat().st_size / 1e3:.0f} KB"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
