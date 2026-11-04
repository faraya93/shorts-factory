"""Rig for 006 (pieles-arrugadas-agua): palette, a stylised fingertip (rounded solid, optional ridge rings), a water tank, a nerve line with signal pulses.
Skin is a chunky matte solid: no skin texture, no blood on screen (vessels are tubes, blood is a few red beads)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402

SKIN, SKIN_DK, VESSEL, BEAD, WATER, SPONGE, MARBLE = "#6E3A28", "#4A2418", "#92202A", "#E24B4B", "#2F7DE6", "#F2C94C", "#6C4FD6"


def palette(S):
    return {"skin": S.hero("big", SKIN, rough=0.6), "skin_dk": S.hero("small", SKIN_DK, rough=0.6), "vessel": S.hero("rubber", VESSEL, rough=0.45),
            "bead": S.hero("mark", BEAD, rough=0.4), "water": S.glass(WATER, alpha=0.45), "sponge": S.hero("housing", SPONGE, rough=0.8, coat=0.0),
            "marble": S.hero("mark", MARBLE, rough=0.15, coat=0.6), "plate": S.plate_mat(), "board": S.board_mat()}


class Finger:
    """Vertical finger, tip down. `root` sits at the tip; the shaft rises along +z. rings: n ridge tori (hidden until show_rings)."""

    def __init__(self, S, M, x, z_tip, name="f", R=1.1, L=7.0, rings=6, **tk):
        self.S, self.R, self.L = S, R, L
        self.root = S.empty(name, (x, 0, z_tip), **tk)
        self.shaft = S.cyl(name + "_sh", R, L, (0, 0, L / 2 + 0.0), M["skin"], axis="Z", parent=self.root, verts=48)
        self.tip = S.ball(name + "_tip", M["skin"], R, (0, 0, 0.0), parent=self.root, seg=32)
        self.rings = [S.torus(f"{name}_r{i}", R + 0.03, 0.09, (0, 0, 0.45 + i * 0.5), M["skin_dk"], parent=self.root, pop=(1e9, 0.3)) for i in range(rings)]
        self.ringset = M

    def show_rings(self, t0, stagger=0.12, dur=0.35):
        for i, r in enumerate(self.rings):
            self.S.pop(r, t0 + stagger * i, dur)


def tank(S, M, x=0.0, w=13.0, d=3.4, h=8.0, z0=0.0, **tk):
    """Translucent water block standing on the floor; returns the box (surface at z0+h)."""
    return S.box("tank", (w, d, h), (x, 0.0, z0 + h / 2), M["water"], bevel=0.25, **tk)


def ripples(S, M, x, z, t0, n=3, dur=1.4, r1=2.6, mat=None):
    """Expanding rings on the water surface (flat tori), staggered."""
    out = []
    for i in range(n):
        o = S.torus(f"rip{i}_{x:.1f}", 1.0, 0.05, (x, 0, z), mat or M["skin_dk"], rot=(math.pi / 2, 0, 0))
        out.append(o)
        a = t0 + i * 0.35
        S.size(o, [(a, 0.2), (a + dur, r1)])
        S.pop(o, a, 0.05)
        S.gone(o, a + dur - 0.4, 0.4)
    return out
