"""Engine spike R3: code3d proof of concept. A software 3D renderer on Pillow only (no 3D library is installed here).

Scene: a skin slab with a shallow cut; a curved needle rotates about its circle centre (as in real suturing): it
enters the skin left of the cut, passes UNDER the cut (hidden) and exits right; then the thread is pulled taut across
the cut and the edges close. Perspective camera, flat shading, painter's order, 1.5x supersampling.
Usage: python spikes/code3d_poc.py <out_dir> [--frames-only t1,t2,...]"""

import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

W, H, FPS, DUR, SS = 1080, 1920, 30, 5.0, 1.5
BG, SKIN, WALL, FLOOR = (226, 213, 241), (242, 196, 168), (217, 140, 132), (201, 112, 111)  # BG = identity spec hex
STEEL, STEEL_HI, THREAD = (190, 196, 208), (250, 250, 255), (20, 20, 24)
CAM, TARGET, FOV = (0.0, 11.0, 7.6), (0.0, 0.0, 0.4), 44.0
CX, CY, R = 0.0, 1.4, 1.9          # needle circle (x-y plane): centre height 1.4 above the skin, radius 1.9
ENTRY_DEG = -150.0                 # tip hovers just above the skin left of the cut
FLOOR_Y, SLAB_X, SLAB_Z = -0.3, 2.4, 7.0

_f = [TARGET[i] - CAM[i] for i in range(3)]
_n = math.sqrt(sum(c * c for c in _f)); _f = [c / _n for c in _f]
_r = [_f[1] * 0 - _f[2] * 1, _f[2] * 0 - _f[0] * 0, _f[0] * 1 - _f[1] * 0]       # forward x up(0,1,0)
_rn = math.sqrt(sum(c * c for c in _r)); _r = [c / _rn for c in _r]
_u = [_r[1] * _f[2] - _r[2] * _f[1], _r[2] * _f[0] - _r[0] * _f[2], _r[0] * _f[1] - _r[1] * _f[0]]
FOCAL = (H * SS) / (2 * math.tan(math.radians(FOV) / 2))


def proj(p):
    d = [p[i] - CAM[i] for i in range(3)]
    x, y, z = (sum(d[i] * v[i] for i in range(3)) for v in (_r, _u, _f))
    return (W * SS / 2 + FOCAL * x / z, H * SS / 2 - FOCAL * y / z), FOCAL / z   # screen point, pixels per world unit


def smooth(a, b, t):
    k = min(1.0, max(0.0, (t - a) / (b - a)))
    return k * k * (3 - 2 * k)


def circ(deg, lift=0.0):
    a = math.radians(deg)
    return (CX + R * math.cos(a), CY + R * math.sin(a) + lift, 0.0)


def tube(d, pts, w0, w1, color, hi=None):
    """A tapered tube from billboarded cylinder segments; only the part above the skin (y >= 0) is visible."""
    n = len(pts)
    for i in range(n - 1):
        a, b = pts[i], pts[i + 1]
        if a[1] < 0 or b[1] < 0:
            continue
        (pa, sa), (pb, sb) = proj(a), proj(b)
        w = w0 + (w1 - w0) * i / max(1, n - 2)
        d.line([pa, pb], fill=color, width=max(2, round(w * (sa + sb) / 2)), joint="curve")
        d.ellipse([pb[0] - w * sb / 2, pb[1] - w * sb / 2, pb[0] + w * sb / 2, pb[1] + w * sb / 2], fill=color)
        if hi:
            d.line([pa, pb], fill=hi, width=max(1, round(w * (sa + sb) / 6)))


def render(t):
    img = Image.new("RGB", (round(W * SS), round(H * SS)), BG)
    d = ImageDraw.Draw(img)
    close = smooth(3.8, 5.0, t)
    gap = 0.7 - 0.62 * close                                     # the cut closes at the end
    quad = lambda pts, c: d.polygon([proj(p)[0] for p in pts], fill=c)
    z0, z1 = -SLAB_Z, SLAB_Z
    quad([(-gap / 2, FLOOR_Y, z0), (gap / 2, FLOOR_Y, z0), (gap / 2, FLOOR_Y, z1), (-gap / 2, FLOOR_Y, z1)], FLOOR)
    quad([(-gap / 2, FLOOR_Y, z0), (-gap / 2, 0, z0), (-gap / 2, 0, z1), (-gap / 2, FLOOR_Y, z1)], WALL)
    quad([(gap / 2, FLOOR_Y, z0), (gap / 2, 0, z0), (gap / 2, 0, z1), (gap / 2, FLOOR_Y, z1)], WALL)
    quad([(-SLAB_X, 0, z0), (-gap / 2, 0, z0), (-gap / 2, 0, z1), (-SLAB_X, 0, z1)], SKIN)
    quad([(gap / 2, 0, z0), (SLAB_X, 0, z0), (SLAB_X, 0, z1), (gap / 2, 0, z1)], SKIN)

    tip = ENTRY_DEG + (25.0 - ENTRY_DEG) * smooth(0.6, 3.0, t)   # needle turns about its circle centre
    away = 4.0 * smooth(3.8, 4.8, t)                              # then the needle is lifted out of the shot
    tail = tip - 140.0
    thread = [(-2.3 + 0.0, 0.02, 0.0)] + [circ(a) for a in _frange(ENTRY_DEG, max(ENTRY_DEG, tail), 2.0)]
    thread += [circ(tail)] if tail > ENTRY_DEG else []
    tube(d, thread, 0.05, 0.05, THREAD)
    shift = (close * 0.3, 0.0)                                    # entry/exit points follow the closing edges
    lift = -0.25 + 0.27 * smooth(3.8, 4.6, t)                     # the stitch surfaces across the closed cut
    xl, xr = -1.285 + shift[0], 1.285 - shift[0]
    tube(d, [(xl, lift, 0.0), (xl + 0.3, lift, 0.0), (xr - 0.3, lift, 0.0), (xr, lift, 0.0)], 0.06, 0.06, THREAD)
    needle = [circ(a, away) for a in _frange(tail, tip, 2.0)] + [circ(tip, away)]
    tube(d, needle, 0.17, 0.03, STEEL, STEEL_HI)
    return img.resize((W, H), Image.LANCZOS)


def _frange(a, b, step):
    n = max(1, int(abs(b - a) / step))
    return [a + (b - a) * i / n for i in range(n + 1)]


if __name__ == "__main__":
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    if "--frames-only" in sys.argv:
        for t in sys.argv[sys.argv.index("--frames-only") + 1].split(","):
            render(float(t)).save(out / f"probe-{float(t):.1f}.png")
        sys.exit(0)
    for i in range(round(DUR * FPS)):
        render(i / FPS).save(out / f"f-{i:04d}.png")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(out / "f-%04d.png"), "-c:v", "libx264",
                    "-crf", "16", "-pix_fmt", "yuv420p", str(out.parent / "r3-code3d.mp4")], check=True)
    print("r3-code3d.mp4 written")
