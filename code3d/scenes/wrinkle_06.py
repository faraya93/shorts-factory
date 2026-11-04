"""pieles-arrugadas 6 (nervio): two fingers in the water; the healthy one wrinkles and its nerve pulses; the other's nerve is cut (red X) and it stays smooth."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import wrinkle_rig as wr  # noqa: E402

S = sp.Shot(163)
M = wr.palette(S)
t_cue, t_ner, t_dan = S.t("cuerpo", default=0.5), S.t("nervio", default=2.0), S.t("dañado,", default=2.8)
wr.tank(S, M, pop=(0.1, 0.5), w=13.0, h=6.5)
XA, XB = -3.4, 3.4
fa = wr.Finger(S, M, XA, 17.0, "fa", rings=6, pop=(0.2, 0.3))
fb = wr.Finger(S, M, XB, 17.0, "fb", rings=6, pop=(0.2, 0.3))
S.move(fa.root, [(0.2, (XA, 0, 17.0)), (1.3, (XA, 0, 3.0))]); S.move(fb.root, [(0.2, (XB, 0, 17.0)), (1.3, (XB, 0, 3.0))])
fa.show_rings(1.6, 0.18, 0.4)                                  # only the healthy finger wrinkles (the rings are the grooves)
# nerves: drawn in front of each finger, running down from above the frame
S.line("nA", [(XA, -1.9, 26.0), (XA, -1.9, 15.0), (XA, -1.9, 9.0)], 0.2, S.accent, grow=(t_ner, t_ner + 0.8), smooth=False)
S.line("nB1", [(XB, -1.9, 26.0), (XB, -1.9, 17.0)], 0.2, S.accent, grow=(t_ner, t_ner + 0.6), smooth=False)
S.line("nB2", [(XB, -1.9, 13.6), (XB, -1.9, 9.0)], 0.2, S.accent, grow=(t_ner + 0.6, t_ner + 1.0), smooth=False)
for j, a in enumerate((t_ner + 0.9, t_ner + 1.5, t_ner + 2.1, t_ner + 2.7)):
    p = S.ball(f"pa{j}", S.accent, 0.5, (XA, -1.9, 22.0), pop=(a, 0.12))
    S.move(p, [(a, (XA, -1.9, 22.0)), (a + 0.6, (XA, -1.9, 9.2))]); S.gone(p, a + 0.5, 0.2)
q = S.ball("pb", S.accent, 0.5, (XB, -1.9, 22.0), pop=(t_ner + 0.9, 0.12))
S.move(q, [(t_ner + 0.9, (XB, -1.9, 22.0)), (t_ner + 1.35, (XB, -1.9, 17.4))]); S.gone(q, t_ner + 1.3, 0.1)
for nm, a in (("xa", 1), ("xb", -1)):
    S.box(nm, (2.4, 0.3, 0.4), (XB, -2.2, 15.3), S.error, bevel=0.12, rot=(0, math.radians(45 * a), 0), pop=(t_dan, 0.3))
wr.ripples(S, M, XA, 6.5, 1.2, n=2, r1=2.2); wr.ripples(S, M, XB, 6.5, 1.2, n=2, r1=2.2)
S.cam([(0, (0, 0, 11), 44, 14, -28), (2.0, (0, 0, 10), 34, 8, 0), (S.T, (0.5, 0, 9.6), 31, 6, 16)])
S.go()
