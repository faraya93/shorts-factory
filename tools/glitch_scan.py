"""Flag frames whose mean luma deviates from BOTH neighbours (render glitches such as black metals): .venv/bin/python tools/glitch_scan.py productions/<ch>/<video> [thr]"""
import subprocess, sys, re
from pathlib import Path
prod = Path(sys.argv[1]); thr = float(sys.argv[2]) if len(sys.argv) > 2 else 1.2
for clip in sorted((prod / "clips").glob("scene-*.mp4")):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(clip), "-vf", "scale=108:192,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-", "-f", "null", "-"], capture_output=True, text=True).stdout
    y = [float(m) for m in re.findall(r"YAVG=([0-9.]+)", out)]
    import statistics
    bad = [i + 1 for i in range(len(y)) if len(y) > 12 and abs(y[i] - statistics.median(y[max(0, i - 8):i] + y[i + 1:i + 9])) > thr]
    print(clip.name, len(y), "frames; suspect:", bad)
