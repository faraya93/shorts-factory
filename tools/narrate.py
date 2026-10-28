"""Write per-scene narration (mp3 + srt + words.json + audio.json hash) for a production WITHOUT clips, using the Editor's own synthesize.
Run: .venv/bin/python tools/narrate.py productions/<channel>/<video>"""
import asyncio, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "factory"))
import editor  # noqa: E402

prod = Path(sys.argv[1]); cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8"))
voice = cfg.get("voice", editor.DEFAULT_VOICE); audio = prod / "audio"; audio.mkdir(exist_ok=True)
meta_path = audio / "audio.json"; meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
for s in cfg["scenes"]:
    n = f"scene-{s['id']:02d}"
    asyncio.run(editor.synthesize(s["narration"], voice, audio / f"{n}.mp3", audio / f"{n}.srt"))
    meta[n] = hashlib.sha256(f"{voice}|{s['narration']}".encode()).hexdigest()
    print(n, round(float(__import__('subprocess').run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(audio/f'{n}.mp3')],capture_output=True,text=True).stdout),2),"s")
meta_path.write_text(json.dumps(meta, indent=2))
