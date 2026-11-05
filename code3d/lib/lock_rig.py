"""Rig for 007 (candado-solo-abre-su-llave): the padlock exterior, a side-view cutaway of a pin-tumbler cylinder (five pin stacks, key that lifts them)
and the key. Geometric hero ('padlock', code-primitive). Everything is drawn with the set-piece kit; the shear line is the accent."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

BRASS, STEEL, DARK, GOLD, WHITE = "#E0A93B", "#A9B2BD", "#0D2B26", "#F2C24A", "#F4EFE0"
XS = [-6.0, -3.0, 0.0, 3.0, 6.0]
LEN = [2.0, 3.0, 1.6, 2.6, 2.2]                 # key-pin lengths
ZS, ZF, ZTOP = 10.0, 7.0, 16.2                  # shear line, plug floor (key-pin rest bottom), spring anchor


def palette(S):
    return {"brass": S.hero("housing", BRASS, rough=0.35, metal=0.6, coat=0.2), "steel": S.hero("blade", STEEL, rough=0.3, metal=0.8, coat=0.1),
            "dark": S.hero("blockm", DARK, rough=0.9, coat=0.0), "gold": S.hero("mark", GOLD, rough=0.35, metal=0.4), "white": S.hero("small", WHITE, rough=0.4),
            "accent": S.emit("#3DFFB0", 1.0, "gold_dim"), "plate": S.hero("plate", DARK, rough=0.9, coat=0.0)}


# ---------------------------------------------------------------- exterior
def padlock(S, M, loc=(0, 0, 0), pop=None):
    root = S.empty("padlock", loc, pop=pop)
    body = S.box("lockbody", (11.0, 4.6, 8.4), (0, 0, 4.2), M["brass"], bevel=1.1, parent=root)
    sh = S.line("shackle", [(-2.9, 0, 7.5), (-2.9, 0, 11.0), (-2.0, 0, 13.4), (0, 0, 14.4), (2.0, 0, 13.4), (2.9, 0, 11.0), (2.9, 0, 7.5)], 0.8, M["steel"])
    sh.parent = root
    S.reg(sh)
    hole = S.cyl("keyhole", 0.95, 0.3, (0, -2.35, 4.9), M["dark"], axis="Y", parent=root, verts=24)
    slot = S.box("keyslot", (0.7, 0.3, 2.0), (0, -2.35, 3.7), M["dark"], bevel=0.05, parent=root)
    return root, body, sh


def key(S, M, loc=(0, 0, 0), name="key", pop=None):
    root = S.empty(name, loc, pop=pop)
    S.box(name + "_blade", (1.0, 6.0, 1.3), (0, 3.4, 0), M["steel"], bevel=0.15, parent=root)
    for i, d in enumerate((1.6, 2.6, 3.6, 4.6)):
        S.box(f"{name}_t{i}", (1.0, 0.45, 0.5 + 0.2 * (i % 2)), (0, d + 0.8, -0.8 - 0.1 * (i % 2)), M["steel"], bevel=0.05, parent=root)
    S.torus(name + "_bow", 1.9, 0.5, (0, -0.6, 0), M["steel"], rot=(math.pi / 2, 0, 0), parent=root)
    return root


# ---------------------------------------------------------------- cutaway
class Cut:
    """Side-view cut of the cylinder. update(t) places the pins from the key position X(t) (the key slides in along +x; X=0 means fully in)."""

    def __init__(self, S, M, wrong=-1, show_key=True, pop=None):
        self.S, self.wrong = S, wrong
        S.box("cplate", (36, 1.0, 28), (0, 2.6, 9.5), M["plate"], bevel=0.4)
        S.box("cbody", (27, 1.4, 17.5), (0, 1.5, 9.6), M["brass"], bevel=0.5, pop=pop)
        S.box("cplug", (24, 0.6, 5.4), (0, 0.5, 7.6), M["steel"], bevel=0.2, pop=pop)
        S.box("ckeyway", (24.2, 0.5, 2.2), (0, 0.15, 6.3), M["dark"], bevel=0.05, pop=pop)
        for x in XS:
            S.box(f"chamber{x}", (2.1, 0.5, 6.4), (x, 0.55, 13.0), M["dark"], bevel=0.1, pop=pop)
        self.kp, self.dr, self.sp = [], [], []
        for i, x in enumerate(XS):
            self.kp.append(S.cyl(f"kpin{i}", 0.85, LEN[i], (x, -0.4, ZF + LEN[i] / 2), M["gold"], axis="Z", verts=24, pop=pop))
            self.dr.append(S.cyl(f"dpin{i}", 0.85, 2.2, (x, -0.4, ZF + LEN[i] + 1.1), M["white"], axis="Z", verts=24, pop=pop))
            self.sp.append(tr.cyl(f"spring{i}", 0.4, 1.0, (x, -0.4, 14.0), M["steel"], axis="Z", verts=16))   # not registered: scaled every frame
        self.line = S.box("shear", (24.4, 0.2, 0.22), (0, -1.0, ZS), M["accent"], bevel=0.02, pop=(1e9, 0.3))
        self.key = None
        if show_key:
            self.key = S.empty("ckey", (-30.0, -0.2, 0))
            self.heights = [ZS - LEN[i] - (1.1 if i == wrong else 0.0) for i in range(5)]
            S.box("ckey_slab", (34.5, 0.6, 1.4), (-8.75, 0, 6.3), M["steel"], bevel=0.15, parent=self.key)
            for i, x in enumerate(XS):
                hz = self.heights[i] - 6.5
                S.box(f"ckey_t{i}", (1.5, 0.6, hz), (x, 0, 6.5 + hz / 2), M["steel"], bevel=0.12, parent=self.key)
        self.X = lambda t: -30.0
        self.gap = lambda t: 0.0
        S.every_frame(self.update)

    def update(self, t):
        X = self.X(t)
        if self.key is not None:
            self.key.location.x = X
        g = self.gap(t)
        for i, x in enumerate(XS):
            lift = 0.0
            if self.key is not None:
                for k, xk in enumerate(XS):
                    d = abs(x - (xk + X))
                    w = max(0.0, min(1.0, (1.5 - d) / 0.7))
                    w = w * w * (3 - 2 * w)
                    lift = max(lift, w * (self.heights[k] - ZF))
            zb = ZF + lift
            self.kp[i].location.z = zb + LEN[i] / 2
            self.dr[i].location.z = zb + LEN[i] + 1.1 + g
            top = zb + LEN[i] + 2.2 + g
            self.sp[i].location.z = (top + ZTOP) / 2
            self.sp[i].scale.z = max(0.05, (ZTOP - top) / 1.0)
