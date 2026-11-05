"""termo 2 (paredes): section of the flask: outer wall, inner wall, an empty gap between them (vacuum)."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import flask_rig as fr  # noqa: E402

S = sp.Shot(165, floor_z=0.0)
M = fr.palette(S)
P = fr.section(S, M)
for s in (0, 1):
    S.pop(P["outer"][s], 0.1, 0.01)
tw = S.t("paredes", default=1.0)
for i, o in enumerate(P["inner"]):
    S.pop(o, tw + 0.5 + 0.1 * i, 0.4)
pulse = S.box("gapglow", (fr.GAP * 0.9, 0.3, 19.0), (fr.XG, -0.4, 10.0), S.hero("pulse", "#3A2BD0", rough=0.5), bevel=0.05, pop=(S.t("aire", default=3.0), 0.3))
pulse2 = S.box("gapglow2", (fr.GAP * 0.9, 0.3, 19.0), (-fr.XG, -0.4, 10.0), S.hero("pulse", "#3A2BD0", rough=0.5), bevel=0.05, pop=(S.t("aire", default=3.0), 0.3))
S.cam([(0, (0, 0, 11), 92, 2, -8), (2.2, (2.5, 0, 12), 50, 1, 0), (S.T, (4.0, 0, 13), 26, 0, 6)])
S.go()
