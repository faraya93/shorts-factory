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

DEFAULT_VOICE = "es-CL-LorenzoNeural"
AUDIO_DEFAULTS = {"narration_volume": 1.0, "effects_volume": 0.30, "music_volume": 0.10,
                  "clip_audio": "off", "clip_gate_db": -35.0, "music_file": None, "music_credit": None}
AUDITION_VOICES =["es-CL-LorenzoNeural", "es-MX-JorgeNeural", "es-ES-AlvaroNeural", "es-CL-CatalinaNeural"]
W, H, FPS = 1080, 1920, 30
MAX_SLOWDOWN = 1.25

# Subtítulos: negrita blanca, contorno negro grueso, centrados en el tercio inferior
# (borde inferior del bloque al 93% de la altura).
FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
SUB_FONT_SIZE = 57          # px
SUB_STROKE = 7              # px, contorno negro
SUB_BOTTOM_Y_FRAC = 0.93    # borde INFERIOR del bloque, como fracción de la altura del frame
SUB_MAX_WIDTH = 940         # px, ancho máximo antes de partir en 2 líneas
SUB_BOTTOM_Y = round(H * SUB_BOTTOM_Y_FRAC)
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


def parse_srt_time(t: str) -> float:
    h, m, rest = t.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def group_cues(tokens: list[str], events: list[dict]) -> list[tuple[float, float, str]]:
    """Agrupa palabras en frases cortas. Los eventos traen tiempos pero no puntuación,
    así que se alinean 1:1 con las palabras del texto original."""
    if len(tokens) != len(events):
        sys.exit(f"ERROR: edge-tts devolvió {len(events)} palabras y el texto tiene {len(tokens)}; "
                 "no se pueden alinear los subtítulos.")
    cues, cur = [], []

    def flush():
        if cur:
            cues.append((cur[0][1], cur[-1][2], " ".join(t for t, _, _ in cur)))
            cur.clear()

    for tok, ev in zip(tokens, events):
        start, end = ev["offset"] / 1e7, (ev["offset"] + ev["duration"]) / 1e7
        if cur and (len(cur) >= CUE_MAX_WORDS or len(" ".join(t for t, _, _ in cur) + " " + tok) > CUE_MAX_CHARS):
            flush()
        cur.append((tok, start, end))
        text = " ".join(t for t, _, _ in cur)
        if re.search(r"[.?!:;]$", tok) or (tok.endswith(",") and len(text) >= 10):
            flush()
    flush()
    # sin huecos entre frases cercanas: cada cue dura hasta el inicio de la siguiente
    out = []
    for i, (s, e, t) in enumerate(cues):
        if i + 1 < len(cues) and cues[i + 1][0] - e < 0.5:
            e = cues[i + 1][0]
        out.append((s, e, t))
    return out


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
    srt.write_text("".join(f"{i}\n{srt_time(s)} --> {srt_time(e)}\n{t}\n\n"
                           for i, (s, e, t) in enumerate(cues, 1)), encoding="utf-8")


def read_srt(path: Path) -> list[tuple[float, float, str]]:
    cues = []
    for block in path.read_text(encoding="utf-8").strip().split("\n\n"):
        lines = block.split("\n")
        a, b = lines[1].split(" --> ")
        cues.append((parse_srt_time(a), parse_srt_time(b), " ".join(lines[2:])))
    return cues


# --- Subtítulos como PNG (este ffmpeg no trae libass/freetype) -------------------------

def render_cue(text: str, path: Path, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    probe_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if line and probe_draw.textlength(trial, font=font) > SUB_MAX_WIDTH:
            lines.append(line)
            line = word
        else:
            line = trial
    lines.append(line)
    block = "\n".join(lines)
    box = probe_draw.multiline_textbbox((0, 0), block, font=font, stroke_width=SUB_STROKE, align="center", spacing=8)
    w, h = math.ceil(box[2] - box[0]) + 2 * SUB_STROKE, math.ceil(box[3] - box[1]) + 2 * SUB_STROKE
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).multiline_text((SUB_STROKE - box[0], SUB_STROKE - box[1]), block, font=font, fill="white",
                                       stroke_width=SUB_STROKE, stroke_fill="black", align="center", spacing=8)
    img.save(path)
    return w, h


# --- Montaje ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("production", type=Path)
    ap.add_argument("--voice", help="edge-tts voice; default: scenes.json 'voice', else " + DEFAULT_VOICE)
    ap.add_argument("--audition", action="store_true",
                    help="render scene 1's narration with each AUDITION_VOICES into audio/audition/ and exit")
    ap.add_argument("--gate-report", action="store_true",
                    help="measure each clip's audio against audio.clip_gate_db, print the table and exit (no render)")
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
    clips, audio_dir, build = prod / "clips", prod / "audio", prod / "build"
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
        if meta.get(n) == digest and (audio_dir / f"{n}.mp3").exists() and (audio_dir / f"{n}.srt").exists():
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
        plan.append({"s": s, "n": n, "slot": slot, "slot_frames": slot_frames, "factor": factor, "freeze": freeze,
                     "has_audio": info["has_audio"], "gate": gate})
        report.append((s["id"], s["name"], narr, slot, d, info["has_audio"], note))

    # 4. Subtítulos globales (cues por escena desplazadas por los slots acumulados) -> PNGs
    font_path = next((f for f in FONT_CANDIDATES if Path(f).exists()), None)
    if not font_path:
        print("ERROR: no encontré una fuente en negrita en FONT_CANDIDATES.")
        return 1
    font = ImageFont.truetype(font_path, SUB_FONT_SIZE)
    for old in build.glob("cue-*.png"):
        old.unlink()
    global_cues, offset = [], 0.0
    for p in plan:
        for a, b, text in read_srt(audio_dir / f"{p['n']}.srt"):
            global_cues.append((offset + a, min(offset + b, offset + p["slot"]), text))
        offset += p["slot"]
    total = offset
    (prod / "final.srt").write_text("".join(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{t}\n\n"
                                            for i, (a, b, t) in enumerate(global_cues, 1)), encoding="utf-8")
    cue_imgs = []
    for i, (a, b, text) in enumerate(global_cues):
        png = build / f"cue-{i:03d}.png"
        cue_imgs.append((png, *render_cue(text, png, font), a, b))

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
    parts = []
    for i, p in enumerate(plan):
        chain = [f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos", f"crop={W}:{H}",
                 "setsar=1", f"fps={FPS}"]
        if p["factor"] != 1.0:
            chain += [f"setpts=PTS*{p['factor']:.6f}", f"fps={FPS}"]
        if p["freeze"] > 0.001:
            chain.append(f"tpad=stop_mode=clone:stop_duration={p['freeze'] + 0.2:.3f}")
        chain += [f"trim=end_frame={p['slot_frames']}", "setpts=PTS-STARTPTS"]
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
    for k, (png, w, h, a, b) in enumerate(cue_imgs):
        x, y = (W - w) // 2, SUB_BOTTOM_Y - h
        parts.append(f"[{last}][{2 * n_sc + k}:v]overlay=x={x}:y={y}:enable='between(t,{a:.3f},{b:.3f})'[o{k}]")
        last = f"o{k}"

    # audio mix: normalize=0 keeps every layer at exactly its configured volume; the limiter only prevents clipping
    parts.append(f"[acat]volume={audio['narration_volume']}[nar]")
    layers = ["[nar]"]
    if fx:
        parts.append(f"[fcat]volume={audio['effects_volume']}[fxv]")
        layers.append("[fxv]")
    if music_path:
        music_idx = 2 * n_sc + len(cue_imgs)
        parts.append(f"[{music_idx}:a]aresample=48000,aformat=channel_layouts=stereo,"
                     f"atrim=duration={total:.5f},asetpts=PTS-STARTPTS,volume={audio['music_volume']}[mus]")
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
    if music_path:
        cmd += ["-stream_loop", "-1", "-i", str(music_path)]
    final = prod / "final.mp4"
    cmd += ["-/filter_complex", str(script), "-map", f"[{last}]", "-map", audio_out,
            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-t", f"{total:.5f}", str(final)]
    print(f"\nCodificando {len(cue_imgs)} subtítulos sobre {total:.1f} s de video ...")
    run(cmd)

    # 6. Portada: escena 1 a ~1 s, limpia (sin subtítulos)
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
    print(f"\nDuración total: {float(out['format']['duration']):.2f} s (timeline {total:.2f} s)")
    print(f"Video: {v['width']}x{v['height']} @ {v['r_frame_rate']} fps, {v['codec_name']} {v['pix_fmt']}")
    print(f"Voz: {voice}")
    print("Audio profile: "
          f"narration x{audio['narration_volume']:.2f} | "
          f"effects {'ACTIVE x%.2f, gate %g dB' % (audio['effects_volume'], audio['clip_gate_db']) if fx else 'OFF (clip audio discarded)'} | "
          f"music {music_note}")
    if music_path and audio.get("music_credit"):
        print(f"Music credit: {audio['music_credit']}")
    print(f"Subtítulos: {len(cue_imgs)} frases | fuente {Path(font_path).name} {SUB_FONT_SIZE}px, contorno {SUB_STROKE}px")
    print(f"final.mp4: {final.stat().st_size / 1e6:.1f} MB | cover.jpg: {(prod / 'cover.jpg').stat().st_size / 1e3:.0f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
