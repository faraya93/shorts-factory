"""micro 1 (hook): see productions/mecanalia-es/022*/script.json. A cutaway microwave with a fork and a spoon on its turning plate; the camera orbits the plate while the fork's tines crackle with arcs and the spoon stays dark."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import micro_rig as mr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(190, floor_z=-0.6)
T_IN = 3.6
n = mr.build(S)
pairs = [(n.tips[j], n.tips[j + 1]) for j in range(3)]
mr.burst_arcs(S, S.accent, "arc_fork", pairs, [(1.2, 0.5), (2.3, 0.5), (3.4, 0.5), (4.5, 0.6), (5.6, 0.7)], parent=n.fork, r=0.3 / mr.CS, amp=1.0 / mr.CS, arch=3.0)


def upd(t):
    mr.spin_plate(n, mr.plate_angle(t, 0.3))
    az = sp.interp([(0, 26.0), (S.T, -4.0)], t)
    rad0 = sp.interp([(0, 225.0), (S.T, 180.0)], t)
    el0 = sp.interp([(0, 22.0), (S.T, 16.0)], t)
    k = sp.interp([(T_IN, 0.0), (S.T, 1.0)], t)                       # from the whole oven, the camera pushes in to the plate where the cutlery lies
    rad = rad0 if t <= T_IN else sp.lerp(sp.interp([(0, 225.0), (S.T, 180.0)], T_IN), 80.0, k)
    el = el0 if t <= T_IN else sp.lerp(sp.interp([(0, 22.0), (S.T, 16.0)], T_IN), 30.0, k)
    mr.look(S, (sp.lerp(-8.0, -11.0, k), sp.lerp(0.0, -2.0, k), sp.lerp(19.0, 6.0, k)), rad, el, az)
    n.lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(-5, -30, 22))
S.go()
