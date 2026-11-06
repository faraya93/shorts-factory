"""latido2 6 (cierre): the heart alone, beating, in one image; the camera pushes in while orbiting."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402
from latido2_common import heart  # noqa: E402

S = sp.Shot(255, floor_z=0.0)
H = heart(S, (0, 0, 0))
rk.softboxes(2.0, centre=(0, 0, 8))
S.cam([(0, (0, 0, 8), 58, 10, -50), (S.T * 0.6, (0, 0, 8), 38, 6, 0), (S.T, (0, 0, 8), 26, 4, 40)])
S.go()
