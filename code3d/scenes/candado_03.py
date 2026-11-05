"""candado 3 (corte): each pin is split; the shear line lights up; the split pins pop apart to show the cut."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import lock_rig as lr  # noqa: E402

S = sp.Shot(180, floor_z=0.0)
M = lr.palette(S)
cut = lr.Cut(S, M, show_key=False)
tl = S.t("linea", default=3.0)
tp = S.t("partido", default=1.2)
import math
cut.gap = lambda t: 0.9 * math.exp(-((t - (tp + 0.4)) / 0.45) ** 2)
cut.line.scale = (1.0, 1.0, 1.0)
S.pop(cut.line, tl, 0.3)
S.cam([(0, (-6, 0, 11.5), 40, 0, -6), (S.T, (6, 0, 11.5), 40, 0, 6)])
S.go()
