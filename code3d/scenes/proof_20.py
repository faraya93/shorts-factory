"""Block B5 asset seal still, earth-globe (not a video scene): the whole globe filling the frame, a slight tilt."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import globe_rig as gr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(30, floor_z=-14.0)
g = gr.Globe(radius=10.0, loc=(0.0, 0.0, 0.0))
g.root.rotation_euler = (math.radians(-18.0), 0.0, 0.0)
g.spin(math.radians(35.0))
S.cam([(0.0, (0.0, 0.0, 0.0), 52.0, 8.0, -12.0), (S.T, (0.0, 0.0, 0.0), 52.0, 8.0, -12.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
