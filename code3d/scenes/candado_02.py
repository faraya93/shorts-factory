"""candado 2 (pinos): the cutaway of the cylinder: five pin stacks held down by springs."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import lock_rig as lr  # noqa: E402

S = sp.Shot(185, floor_z=0.0)
M = lr.palette(S)
cut = lr.Cut(S, M, show_key=False)
S.cam([(0, (0, 0, 11), 86, 2, -10), (3.0, (0, 0, 11.5), 58, 1, 0), (S.T, (0, 0, 12), 42, 0, 8)])
S.go()
