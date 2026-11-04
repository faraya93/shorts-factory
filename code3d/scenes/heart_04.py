"""corazon 4 (minuto): a closed loop tube with beads going all the way round in about a minute (compressed), while a jug fills with 5 litres."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import heart_rig as hr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(214)
M = hr.palette(S)
t_cin, t_cue, t_vue = S.t("cinco", default=1.1), S.t("cuerpo:", default=3.6), S.t("vuelta", default=4.4)
R, CZ = 6.5, 9.0
S.box("floor", (30.0, 10.0, 0.6), (0, 0, -0.3), M["plate"], bevel=0.25, pop=(0.05, 0.4))
loop = S.torus("loop", R, 0.38, (0, 0, CZ), M["glass"], rot=(math.pi / 2, 0, 0), pop=(0.2, 0.5))
heart = hr.pump_heart(S, M, (0, 0, CZ - R - 0.0), scale=0.5, pop=0.4, t_beat=0.6, amp=0.12)
bead = S.ball("bead", M["fluid"], 0.42, (0, 0, 0), seg=14)
NB = 44
def pos(a):
    return (R * math.sin(a), 0.0, CZ - R * math.cos(a))
def beads(i, t):
    if t < 0.5 + 0.02 * i:
        return None
    base = 2 * math.pi * i / NB
    sp_ = 0.5 if t < t_vue - 0.6 else 0.5 + 0.0
    turn = c.smooth(t_vue - 0.6, t_vue + 1.6, t) * 2 * math.pi
    a = base + 0.4 * t + turn
    return pos(a), 1.0
S.swarm(NB, bead, beads)
jug = S.box("jug", (4.0, 3.0, 5.0), (11.0, 0, 2.5), M["glass"], bevel=0.3, pop=(0.5, 0.4))
jf = S.box("jugf", (3.6, 2.6, 1.0), (11.0, 0, 0.3), M["fluid"], bevel=0.15, pop=(0.6, 0.3))
def fill(t):
    k = max(1e-3, 4.4 * c.smooth(t_cin, t_vue + 1.4, t))
    jf.scale = (1.0, 1.0, k)
    jf.location = (11.0, 0, 0.1 + k / 2)
S.every_frame(fill)
S.line("hose", [(R * 0.1, -0.2, CZ - R), (4.0, -0.2, 3.0), (9.0, -0.2, 4.0), (11.0, -0.2, 5.8)], 0.15, S.accent, grow=(t_cin, t_cin + 1.0))
timer = S.torus("timer", 1.3, 0.1, (0, -0.8, CZ), S.accent, rot=(math.pi / 2, 0, 0), pop=(t_cue, 0.3))
hand = S.box("hand", (0.18, 0.18, 1.2), (0, -0.9, CZ), S.accent, bevel=0.05, pop=(t_cue, 0.3))
S.every_frame(lambda t: (setattr(hand, "rotation_euler", (0, -(t - t_cue) / 1.6 * 2 * math.pi, 0)), setattr(hand, "location", (0.6 * math.sin((t - t_cue) / 1.6 * 2 * math.pi), -0.9, CZ + 0.6 * math.cos((t - t_cue) / 1.6 * 2 * math.pi)))))
S.cam([(0, (3, 0, 8), 40, 10, -22), (t_cin, (4, 0, 7), 34, 8, -6), (t_vue, (3, 0, 8), 30, 6, 12), (S.T, (3, 0, 7), 44, 18, 28)])
S.go()
