"""Shared kit for the abstract-machine productions (flavour mixer, reward loop): word-locked timing, bars, spheres, token streams, gauges, lamps.
All geometry lives in the world XZ plane (camera looks along +y); smaller y is nearer the camera."""
import json
import math
import re
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402

FALLBACK_INK, FALLBACK_BOARD = "#1E1E22", "#CFC1A6"


def clean(w):
    return re.sub(r"[^\wáéíóúñü]", "", w.lower())


class Words:
    """Spoken-word start times of one scene: W.t('palta') = first start, W.t('palta', 1) = second occurrence; missing word -> default."""

    def __init__(self, production, n):
        f = Path(production) / "audio" / f"scene-{n:02d}.words.json"
        self.w = []
        if f.exists():
            for ph in json.load(open(f)):
                for w in ph["words"]:
                    self.w.append((clean(w["text"]), w["start"]))

    def t(self, word, k=0, default=0.0):
        hits = [s for (x, s) in self.w if x == clean(word)]
        return hits[k] if len(hits) > k else default


def keys(t, pts):
    if t <= pts[0][0]:
        return pts[0][1]
    for (ta, va), (tb, vb) in zip(pts, pts[1:]):
        if t <= tb:
            k = (t - ta) / (tb - ta) if tb > ta else 1.0
            return va + (vb - va) * k * k * (3 - 2 * k)
    return pts[-1][1]


def path_point(pts, s):
    segs = list(zip(pts, pts[1:]))
    ls = [math.dist(a, b) for a, b in segs]
    d = max(0.0, min(1.0, s)) * sum(ls)
    for (a, b), l in zip(segs, ls):
        if d <= l:
            k = d / l if l else 0.0
            return a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k
        d -= l
    return pts[-1]


def materials():
    """Ink plinth and board from the active identity + the support colours of the production."""
    import looks
    p = looks.current()
    return {"ink": tr.plain("ink", p["plinth"] if p else FALLBACK_INK, rough=0.55),
            "board": tr.plain("g_board", p["support_board"] if p else FALLBACK_BOARD, rough=0.7),
            "plate": tr.plain("plate", p["support_plate"] if p else "#F0E6D2", rough=0.6)}


def setup():
    fl = bpy.data.objects.get("floor")
    if fl:
        fl.hide_render = True
    mats = materials()
    tr.rbox("plinth", (18.0, 4.0, 1.2), (0.0, 0.6, -0.6), mats["ink"], bevel=0.3)
    return mats


def board(mats, z0, w=10.6, h=12.8, y=0.9):
    return tr.rbox("board", (w, 0.4, h), (0.0, y, z0), mats["board"], bevel=0.2)


def bar(name, mat, p0, p1, w=0.5, d=0.5, y=0.0):
    """Bevelled bar between two XZ points."""
    L = math.dist(p0, p1)
    ang = -math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    return tr.rbox(name, (L + w * 0.0, d, w), ((p0[0] + p1[0]) / 2, y, (p0[1] + p1[1]) / 2), mat, bevel=min(0.12, w * 0.4), rot=(0, ang, 0))


def sphere(name, mat, r, loc=(0, 0, 0), shape=(1, 1, 1), parent=None, seg=24):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = shape
    tr._finish(o, mat)
    if parent:
        o.parent = parent
    return o


def hide(o, hidden=True):
    if "_s" not in o:
        o["_s"] = list(o.scale)
    s = o["_s"]
    k = 1e-4 if hidden else 1.0
    o.scale = (s[0] * k, s[1] * k, s[2] * k)


def scale_to(o, k):
    if "_s" not in o:
        o["_s"] = list(o.scale)
    s = o["_s"]
    k = max(1e-4, k)
    o.scale = (s[0] * k, s[1] * k, s[2] * k)


class Stream:
    """n small tokens travelling a polyline in a loop; `amount` (0..1) is the fraction of tokens that exist."""

    def __init__(self, name, mat, pts, n=8, r=0.17, y=-0.1):
        self.pts, self.n, self.y = pts, n, y
        self.o = [sphere(f"{name}{i}", mat, r, (0, y, 0)) for i in range(n)]
        for o in self.o:
            o["_s"] = list(o.scale)
            o.scale = (1e-4,) * 3

    def set(self, t, t_on, t_off, speed=0.35, amount=1.0, grow=0.25):
        for i, o in enumerate(self.o):
            live = t_on <= t <= t_off and i < round(amount * self.n + 1e-6)
            if not live:
                scale_to(o, 1e-4)
                continue
            s = ((t - t_on) * speed + i / self.n) % 1.0
            x, z = path_point(self.pts, s)
            o.location = (x, self.y, z)
            fade = min(1.0, (t - t_on) / grow, (t_off - t) / grow)
            scale_to(o, max(1e-4, fade))


class Gauge:
    """Vertical slot (ink) with stacked coloured segments; set(heights) lays the segments bottom-up."""

    def __init__(self, x, z_bottom, height, mats, seg_mats, width=1.5, y=-0.15):
        self.x, self.zb, self.h, self.y = x, z_bottom, height, y
        self.slot = tr.rbox("slot", (width + 0.45, 0.4, height + 0.4), (x, y + 0.3, z_bottom + height / 2), mats["ink"], bevel=0.2)
        self.seg = [tr.rbox(f"seg{i}", (width, 0.7, 1.0), (x, y - 0.05, z_bottom), m, bevel=0.12) for i, m in enumerate(seg_mats)]
        for o in self.seg:
            o.scale = (1e-4, 1e-4, 1e-4)

    def set(self, hs):
        z = self.zb + 0.1
        for o, h in zip(self.seg, hs):
            h = max(0.0, h)
            if h < 0.06:
                o.scale = (1e-4, 1e-4, 1e-4)
                continue
            o.scale = (1.0, 1.0, h)
            o.location = (self.x, self.y - 0.05, z + h / 2)
            z += h
        return z


def lamp(name, m_on, m_off, x, z, r=0.42, y=-0.2):
    """A lamp = two stacked spheres (off, on); light(k) swaps by scale."""
    off = sphere(name + "_off", m_off, r, (x, y, z))
    on = sphere(name + "_on", m_on, r * 1.02, (x, y - 0.02, z))
    on["_s"] = list(on.scale)
    on.scale = (1e-4,) * 3
    return off, on


def lit(pair, k):
    scale_to(pair[1], 1.0 if k >= 0.5 else 1e-4)


def pop(o, t, t0, dur=0.4):
    s = 1e-4 if t < t0 else max(1e-4, tr.back((t - t0) / dur))
    if "_s" not in o:
        o["_s"] = list(o.scale)
    b = o["_s"]
    o.scale = (b[0] * s, b[1] * s, b[2] * s)
    return s
