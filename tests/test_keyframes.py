"""animate_keyframes must produce exactly the requested duration, size and fps (local ffmpeg only, no spend).
Run: python tests/test_keyframes.py"""

import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "factory"))
from keyframes import animate_keyframes  # noqa: E402
from PIL import Image  # noqa: E402


def test_animation_matches_requested_duration():
    with tempfile.TemporaryDirectory() as d:
        stills = []
        for i, color in enumerate(((200, 60, 60), (60, 200, 60), (60, 60, 200), (200, 200, 60))):
            path = Path(d) / f"key-{i:02d}.png"
            Image.new("RGB", (576, 1024), color).save(path)
            stills.append(path)
        out = Path(d) / "out.mp4"
        animate_keyframes(stills, 6.0, out)
        info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                               "stream=width,height,r_frame_rate:format=duration", "-of", "csv=p=0", str(out)],
                              capture_output=True, text=True).stdout.split()
        assert "1080,1920,30/1" in info[0], info
        assert abs(float(info[1]) - 6.0) < 0.1, info


if __name__ == "__main__":
    test_animation_matches_requested_duration()
    print("ok  test_animation_matches_requested_duration")
