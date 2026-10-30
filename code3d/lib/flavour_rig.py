"""Hero rig of the 'why we do not taste the same' video: ONE stylised avocado half (identical in every comparison) feeds three person-columns.
Each column = three sensor towers (TASTE indigo, SMELL lime, TEXTURE butter; tower height/dome size = that person's gain) and a gauge stacking the three signals.
Not anatomy: abstract sensors and tokens only."""
import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402

TASTE_HEX, SMELL_HEX, TEX_HEX = "#4A2BC4", "#C5DB4A", "#F5D26B"
SKIN_HEX, FLESH_HEX, PIT_HEX = "#35662E", "#C9D96A", "#7A4A2A"
FLESH_RIPE, FLESH_OVER, SKIN_OVER = "#C9D96A", "#9C7B3C", "#4A3A22"
FOAM_HEX, CILANTRO_HEX = "#FFFFFF", "#3E8E3A"
Z0 = 6.0
COLS = (-3.6, 0.0, 3.6)
AVOCADO_AT = (0.0, Z0 + 4.5)
# per-person gains (taste, smell, texture): P1 bitter/green, P2 creamy fat, P3 almost no aroma
GAINS = {0: (1.9, 1.0, 0.8), 1: (0.7, 1.0, 1.8), 2: (1.0, 0.15, 1.0)}
BASE = (0.35, 0.5, 0.9)          # what the avocado carries: taste, smell, texture
UNIT = 1.55


def mats():
    base = mk.setup()
    base.update({"taste": tr.plain("g_pin", TASTE_HEX, rough=0.35, coat=0.2), "smell": tr.plain("microbe", SMELL_HEX, rough=0.4, coat=0.2),
                 "tex": tr.plain("mag_s", TEX_HEX, rough=0.35, coat=0.2),
                 "skin": tr.plain("g_big", SKIN_HEX, rough=0.5), "flesh": tr.plain("waste", FLESH_HEX, rough=0.45),
                 "pit": tr.plain("g_mark", PIT_HEX, rough=0.4), "foam": tr.plain("foam", FOAM_HEX, rough=0.3),
                 "leaf": tr.plain("alu", CILANTRO_HEX, rough=0.5), "off": tr.plain("ink2", "#3A3852", rough=0.5)})
    return base


class Avocado:
    """Half avocado seen from the cut side: skin pear, flesh pear in front, pit."""

    def __init__(self, m, loc=AVOCADO_AT, size=0.75):
        self.root = tr.empty("avocado", (loc[0], 0.0, loc[1]))
        self.m = m
        for tag, mat, k, y in (("skin", m["skin"], 1.0, 0.0), ("flesh", m["flesh"], 0.8, -0.28)):
            for i, (dz, r, sy) in enumerate(((-0.6, 1.45, 0.55), (-0.2, 1.4, 0.55), (0.2, 1.22, 0.55), (0.6, 1.05, 0.55), (0.95, 0.9, 0.55), (1.2, 0.78, 0.55))):
                mk.sphere(f"{tag}{i}", mat, r * k, (0, y, dz), shape=(1, sy, 1), parent=self.root)
        mk.sphere("pit", m["pit"], 0.62, (0, -0.62, -0.5), parent=self.root)
        self.size = size
        self.root.scale = (size,) * 3

    def pop(self, t, t0):
        s = 1e-4 if t < t0 else max(1e-4, tr.back((t - t0) / 0.5))
        self.root.scale = (s * self.size,) * 3

    def ripeness(self, k):
        """0 firm / ripe -> 1 overripe: flesh and skin colours move toward brown (base colours only)."""
        def set_col(mat, a, b):
            ca, cb = c.linear(a), c.linear(b)
            col = tuple(ca[i] + (cb[i] - ca[i]) * k for i in range(3)) + (1.0,)
            mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = col
        set_col(self.m["flesh"], FLESH_RIPE, FLESH_OVER)
        set_col(self.m["skin"], SKIN_HEX, SKIN_OVER)


class Person:
    """One column: three sensor towers + a gauge. gain=(taste, smell, texture)."""

    def __init__(self, idx, m, a, towers=True):
        self.idx, self.m, self.x = idx, m, COLS[idx]
        self.gain = list(GAINS[idx])
        self.gauge = mk.Gauge(self.x, Z0 - 5.0, 5.0, m, [m["taste"], m["smell"], m["tex"]])
        self.towers, self.stems = [], []
        for ch, mat in enumerate((m["taste"], m["smell"], m["tex"])):
            tx = self.x + (ch - 1) * 1.15
            stem = tr.rbox(f"stem{idx}{ch}", (0.28, 0.4, 1.0), (tx, -0.1, Z0 + 1.5), m["ink"], bevel=0.08)
            dome = mk.sphere(f"dome{idx}{ch}", mat, 0.46, (tx, -0.2, Z0 + 2.0))
            self.towers.append((stem, dome, tx))
        self.streams = []
        for ch, mat in enumerate((m["taste"], m["smell"], m["tex"])):
            tx = self.towers[ch][2]
            pts = [AVOCADO_AT, (tx, Z0 + 2.0), (self.x, Z0 + 0.6)]
            self.streams.append(mk.Stream(f"tok{idx}{ch}", mat, pts, n=6, r=0.15))
        self.set_gain(self.gain)

    def set_gain(self, g):
        self.gain = list(g)
        for (stem, dome, tx), gk in zip(self.towers, g):
            h = 0.3 + 0.45 * gk
            stem.scale = (1.0, 1.0, h)
            stem.location = (tx, -0.1, Z0 + 1.0 + h / 2)
            dome.location = (tx, -0.2, Z0 + 1.0 + h + 0.25)
            dome.scale = (0.7 + 0.3 * gk,) * 3

    def signal(self, a=BASE):
        return [a[i] * self.gain[i] for i in range(3)]

    def play(self, t, t_on, t_off, a=BASE, fill=True, fill_dur=2.5):
        sig = self.signal(a)
        for i, s in enumerate(self.streams):
            s.pts = [AVOCADO_AT, (self.towers[i][2], self.towers[i][1].location[2]), (self.x, Z0 + 0.6)]
            s.set(t, t_on, t_off, amount=min(1.0, sig[i] / 1.8) if sig[i] > 0.02 else 0.0)
        if fill:
            k = mk.keys(t, [(t_on + 0.8, 0.0), (t_on + 0.8 + fill_dur, 1.0)])
            self.gauge.set([UNIT * s * k for s in sig])


    def play_ch(self, t, ch, t_on, t_off, a=BASE, fill_dur=2.0):
        """One channel only; returns its gauge height."""
        sig = self.signal(a)[ch]
        st = self.streams[ch]
        st.pts = [AVOCADO_AT, (self.towers[ch][2], self.towers[ch][1].location[2]), (self.x, Z0 + 0.6)]
        st.set(t, t_on, t_off, amount=min(1.0, sig / 1.8) if sig > 0.02 else 0.0)
        return UNIT * sig * mk.keys(t, [(t_on + 0.6, 0.0), (t_on + 0.6 + fill_dur, 1.0)])


def cilantro(m, loc=(0.0, Z0 + 4.5)):
    root = tr.empty("cilantro", (loc[0], 0.0, loc[1]))
    tr.rbox("stem", (0.22, 0.3, 2.0), (0, 0, -0.5), m["leaf"], bevel=0.08, parent=root)
    for i, (dx, dz) in enumerate(((-0.6, 0.7), (0.6, 0.7), (0.0, 1.2))):
        mk.sphere(f"leaf{i}", m["leaf"], 0.55, (dx, -0.1, dz), shape=(1, 0.35, 0.8), parent=root)
    return root
