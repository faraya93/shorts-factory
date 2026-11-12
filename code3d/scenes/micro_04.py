"""micro 4 (chispa): see productions/mecanalia-es/022*/script.json. The air at the tines breaks down: arcs leap between the glowing tips with a flash and a miniature bolt rises from the tines to the cavity ceiling; the camera starts tight on the tips and snaps back to the whole cavity as the first spark breaks."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import micro_rig as mr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(210, floor_z=-0.6)
n = mr.build(S)
TF = mr.fork_pt((11.7, 0.0, 0.8), 0.0)
n.m.halo_k(0.6)
BURSTS = [S.t("rompe", default=1.6), S.t("chispa,", default=3.3), S.t("rayo", default=4.2)]
for j in range(4):
    S.ball(f"tipglow_{j}", S.accent, 0.45, n.tips[j], shape=(1.0, 1.0, 0.8), parent=n.fork)
pairs = [(n.tips[j], n.tips[j + 1]) for j in range(3)]
mr.burst_arcs(S, S.accent, "arc_fork", pairs, [(t0, 0.9) for t0 in BURSTS], parent=n.fork, r=0.1 / mr.CS, amp=0.7 / mr.CS, arch=3.0, core=n.m.core)
top = (TF[0] + 2.0, TF[1] + 2.0, mr.CZ1 - 0.6)                                    # the miniature bolt: from the tines up to the ceiling of the cavity
mr.burst_arcs(S, S.accent, "arc_bolt", [(TF, top), ((TF[0] - 1.0, TF[1], TF[2]), (TF[0] - 5.0, TF[1] + 3.0, mr.CZ1 - 0.6))], [(t0, 0.9) for t0 in BURSTS],
              r=0.9, amp=4.0, arch=0.0, seed=5, core=n.m.core)


def upd(t):
    mr.spin_plate(n, 0.0)
    k = sp.interp([(BURSTS[0] - 0.4, 0.0), (BURSTS[0] + 0.3, 1.0)], t)
    rad = sp.lerp(26.0, 185.0, k)
    el = sp.lerp(46.0, 14.0, k)
    tgt = tuple(sp.lerp(a, b, k) for a, b in zip((TF[0], TF[1] + 3.0, TF[2]), (-8.0, 0.0, 19.0)))
    mr.look(S, tgt, rad, el, sp.lerp(8.0, 22.0, k))
    n.lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(-5, -30, 22))
S.go()
