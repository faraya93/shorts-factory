"""Reward-loop machine for the alcohol video: an abstract, non-anatomical machine, seen twice (A and B) with identical parts and different factory settings.
Parts per machine: a frosted closed bottle (the trigger), a four-node loop (SEÑAL -> DESEO -> BEBIDA -> ALIVIO) with signal tokens, a shortcut track that
appears with repetition, a row of cue lamps, an effect gauge with a target mark (tolerance) and three sliders REWARD / BRAKE / STRESS."""
import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402

Z0 = 6.0
CZ = {0: Z0 + 2.9, 1: Z0 - 2.9}
BOTTLE_X, GAUGE_X = -4.5, -2.9
LOOP_C, HALF = (0.3, 1.45), 1.45
SLIDER_X = (3.5, 4.35, 5.2)
REWARD_HEX, BRAKE_HEX, STRESS_HEX, BOTTLE_HEX, TOKEN_HEX = "#4A2BC4", "#F5D26B", "#A25FC9", "#5B7FD0", "#C5DB4A"
SETTINGS = {0: (0.25, 0.85, 0.2), 1: (0.8, 0.25, 0.8)}      # reward, brake, stress (0..1) per machine


def mats():
    base = mk.setup()
    base.update({"reward": tr.plain("g_pin", REWARD_HEX, rough=0.35, coat=0.2), "brake": tr.plain("mag_s", BRAKE_HEX, rough=0.35, coat=0.2),
                 "stress": tr.plain("wipe", STRESS_HEX, rough=0.4), "bottle": tr.plain("g_big", BOTTLE_HEX, rough=0.9),
                 "token": tr.plain("waste", TOKEN_HEX, rough=0.4, coat=0.2), "off": tr.plain("ink2", "#3A3852", rough=0.5)})
    return base


class Machine:
    def __init__(self, idx, m, M):
        self.idx, self.m, self.M = idx, m, M
        cz = CZ[idx]
        self.cz = cz
        lx, lz = LOOP_C[0], cz
        h = HALF
        # corners in loop order: SEÑAL (top right) -> DESEO (bottom right) -> BEBIDA (bottom left) -> ALIVIO (top left)
        self.corner = [(lx + h, lz + h), (lx + h, lz - h), (lx - h, lz - h), (lx - h, lz + h)]
        self.tracks = []
        for i in range(4):
            a, b = self.corner[i], self.corner[(i + 1) % 4]
            self.tracks.append(mk.bar(f"trk{idx}{i}", M["ink"], a, b, w=0.34, d=0.34, y=-0.05))
        self.nodes = [mk.sphere(f"nd{idx}{i}", M["plate"], 0.46, (p[0], -0.35, p[1])) for i, p in enumerate(self.corner)]
        # shortcut SEÑAL -> BEBIDA (grows with repetition)
        self.short = mk.bar(f"short{idx}", M["ink"], self.corner[0], self.corner[2], w=0.34, d=0.34, y=-0.05)
        mk.hide(self.short)
        # bottle: frosted body + neck + cap, feeder to BEBIDA
        self.bottle = tr.empty(f"bottle{idx}", (BOTTLE_X, 0.0, cz))
        tr.rbox(f"bb{idx}", (1.15, 0.8, 1.8), (0, -0.2, -0.3), M["bottle"], bevel=0.3, parent=self.bottle)
        tr.rbox(f"bn{idx}", (0.5, 0.6, 0.8), (0, -0.2, 0.85), M["bottle"], bevel=0.15, parent=self.bottle)
        tr.rbox(f"bc{idx}", (0.62, 0.65, 0.22), (0, -0.2, 1.35), M["ink"], bevel=0.08, parent=self.bottle)
        self.feeder = mk.bar(f"feed{idx}", M["ink"], (BOTTLE_X + 0.6, cz - h), self.corner[2], w=0.26, d=0.3, y=-0.05)
        # cue lamps above the loop
        self.cues = [mk.lamp(f"cue{idx}{i}", m.gold, M["off"], lx - 1.2 + i * 0.6, cz + h + 1.1, r=0.24) for i in range(5)]
        # effect gauge with target mark
        self.gauge = mk.Gauge(GAUGE_X, cz - 1.7, 3.4, M, [M["token"]], width=0.7)
        self.target = tr.rbox(f"tgt{idx}", (1.05, 0.9, 0.12), (GAUGE_X, -0.3, cz + 0.3), M["brake"], bevel=0.04)
        # sliders
        self.knobs = []
        for k, (x, mat) in enumerate(zip(SLIDER_X, (M["reward"], M["brake"], M["stress"]))):
            tr.rbox(f"sl{idx}{k}", (0.22, 0.3, 3.6), (x, -0.05, cz), M["ink"], bevel=0.08)
            knob = tr.rbox(f"kn{idx}{k}", (0.72, 0.5, 0.42), (x, -0.4, cz), mat, bevel=0.14)
            self.knobs.append(knob)
        self.set_sliders(SETTINGS[idx])
        # tokens
        self.full = mk.Stream(f"tkf{idx}", M["token"], self.corner + [self.corner[0]], n=6, r=0.17, y=-0.55)
        self.cut = mk.Stream(f"tkc{idx}", M["token"], [self.corner[0], self.corner[2], self.corner[3], self.corner[0]], n=4, r=0.17, y=-0.55)

    def set_sliders(self, s):
        for k, knob in enumerate(self.knobs):
            knob.location = (SLIDER_X[k], -0.4, self.cz - 1.5 + 3.0 * s[k])

    def track_depth(self, k):
        """Tracks get deeper (thicker toward the camera) with repetition."""
        for tkr in self.tracks + [self.short]:
            if "_s" not in tkr:
                tkr["_s"] = list(tkr.scale)
            b = tkr["_s"]
            tkr.scale = (b[0], b[1] * (1.0 + 1.6 * k), b[2] * (1.0 + 0.6 * k))

    def cue_all(self, k):
        for p in self.cues:
            mk.lit(p, k)


def phase(speed_fn, t, dt=1 / 30):
    """Integrated loop phase (so a changing speed never makes tokens jump)."""
    ph, x = 0.0, 0.0
    while x < t:
        ph += speed_fn(x) * dt
        x += dt
    return ph


def run_tokens(stream, ph, t, t_on, amount=1.0, grow=0.3):
    for i, o in enumerate(stream.o):
        live = t >= t_on and i < round(amount * stream.n + 1e-6)
        if not live:
            mk.scale_to(o, 1e-4)
            continue
        x, z = mk.path_point(stream.pts, (ph + i / stream.n) % 1.0)
        o.location = (x, stream.y, z)
        mk.scale_to(o, max(1e-4, min(1.0, (t - t_on) / grow)))
