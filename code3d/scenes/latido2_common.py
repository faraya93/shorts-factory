"""Shared helpers for the latido2 scenes (not a scene)."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import asset_rig as ar  # noqa: E402
import bottle_rig as br0  # noqa: E402
import real_kit as rk  # noqa: E402
import bottle_real as bt  # noqa: E402


def heart(S, loc=(0, 0, 0)):
    h = ar.load(S, "human-heart", loc=loc, k=100.0)
    obj = h.objs[0]
    ar.retint(obj, "#C8323C", role="g_big", rough=0.4)
    base = tuple(obj.scale)

    def beat(t):
        s = 1.0 + 0.09 * br0.beat_amount(t)
        obj.scale = (base[0] * s, base[1] * s, base[2] * s)
    S.every_frame(beat)
    return h


def slugs(S, pts, t0, n=14, period=0.83, travel=1.4, r=0.34):
    """Red slugs travelling along the tube from t0 on, one per heartbeat."""
    mat = rk.wet_tissue("g_mark", "#C8323C", sss=0.3, rough=0.25, coat=0.9)
    tpl = S.ball("slug_tpl", mat, r, (0, 0, 0))

    def fn(i, t):
        u = (t - (t0 + period * i)) / travel
        if u < 0 or u > 1:
            return None
        return (bt.path_point(pts, u), 1.0)
    return S.swarm(n, tpl, fn)


def bottle_field(S, items, red=True):
    """Many real bottles that GROW into place. items = [(x, y, z, t_appear, grow_s)]. One template (shell, liquid, cap) cloned by swarms; returns nothing."""
    P = bt.parts(S, (0, 0, -300))
    for key, off in (("shell", 0.0), ("liquid", 0.0), ("cap", bt.H_TOT + 0.4)):
        src = P[key]
        if key == "cap":
            src.location = (0, 0, -300 + off)

        def fn(i, t, off=off):
            x, y, z, ta, gd = items[i]
            if t < ta:
                return None
            k = max(0.03, min(1.0, (t - ta) / gd))
            return ((x, y, z + off * k), k)
        S.swarm(len(items), src, fn)
