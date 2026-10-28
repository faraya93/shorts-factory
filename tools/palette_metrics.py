"""Design-system metrics (pure Python): WCAG contrast, CIEDE2000, hero-colour separation per stage candidate. Run: python tools/palette_metrics.py"""
import math

def rgb(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def lin(c): c /= 255; return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def lum(h): r, g, b = (lin(x) for x in rgb(h)); return 0.2126 * r + 0.7152 * g + 0.0722 * b
def wcag(a, b): la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)
def lab(h):
    r, g, b = (lin(x) for x in rgb(h))
    x, y, z = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047, 0.2126729 * r + 0.7151522 * g + 0.0721750 * b, (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)
def de2000(h1, h2):
    L1, a1, b1 = lab(h1); L2, a2, b2 = lab(h2)
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2); Cm = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cm ** 7 / (Cm ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360; h2p = math.degrees(math.atan2(b2, a2p)) % 360
    dL, dC = L2 - L1, C2p - C1p
    dh = h2p - h1p
    if C1p * C2p == 0: dh = 0
    elif dh > 180: dh -= 360
    elif dh < -180: dh += 360
    dH = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dh / 2))
    Lm, Cmp = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0: hm = h1p + h2p
    elif abs(h1p - h2p) <= 180: hm = (h1p + h2p) / 2
    else: hm = (h1p + h2p + 360) / 2 if h1p + h2p < 360 else (h1p + h2p - 360) / 2
    T = 1 - 0.17 * math.cos(math.radians(hm - 30)) + 0.24 * math.cos(math.radians(2 * hm)) + 0.32 * math.cos(math.radians(3 * hm + 6)) - 0.20 * math.cos(math.radians(4 * hm - 63))
    dth = 30 * math.exp(-(((hm - 275) / 25) ** 2)); Rc = 2 * math.sqrt(Cmp ** 7 / (Cmp ** 7 + 25 ** 7))
    Sl = 1 + 0.015 * (Lm - 50) ** 2 / math.sqrt(20 + (Lm - 50) ** 2); Sc = 1 + 0.045 * Cmp; Sh = 1 + 0.015 * Cmp * T
    Rt = -math.sin(math.radians(2 * dth)) * Rc
    return math.sqrt((dL / Sl) ** 2 + (dC / Sc) ** 2 + (dH / Sh) ** 2 + Rt * (dC / Sc) * (dH / Sh))

HEROES = {"yellow tape": "#F2BD12", "red thermos": "#CC2229", "white appliance": "#F2F1EE", "black remote/phone": "#151517",
          "orange cone/drill": "#F28A1E", "green bottle": "#3FA34D", "blue pen/jeans": "#2E6FD6", "pink": "#E8719A",
          "mid grey tool": "#8A8F96", "steel/silver": "#C8CBD0", "purple": "#7A4FBF", "brown wood": "#7B4A2A"}
STAGES = {"A near-black": "#120F10", "E dark teal": "#0B2A2F", "D0 celeste": "#B9DCF0", "D1 celeste deeper": "#9CCBEA",
          "D2 celeste mid": "#A9D4EE", "D3 cornflower": "#8DB8E8", "B2 warm": "#D5C0A2"}
if __name__ == "__main__":
    print("dE2000 hero vs stage (>=25 clearly distinct, 15-25 weak, <15 merges):")
    print(f"{'hero':20s}" + "".join(f"{s[:12]:>14s}" for s in STAGES))
    for n, h in HEROES.items():
        print(f"{n:20s}" + "".join(f"{de2000(h, s):14.1f}" for s in STAGES.values()))
    print("\ncount of heroes with dE2000 < 20:", {s: sum(de2000(h, v) < 20 for h in HEROES.values()) for s, v in STAGES.items()})


def lab2hex(L, a, b):
    fy = (L + 16) / 116; fx = fy + a / 500; fz = fy - b / 200
    inv = lambda t: t ** 3 if t ** 3 > 216 / 24389 else (116 * t - 16) / (24389 / 27)
    x, y, z = 0.95047 * inv(fx), inv(fy), 1.08883 * inv(fz)
    r = 3.2404542 * x - 1.5371385 * y - 0.4985314 * z; g = -0.9692660 * x + 1.8760108 * y + 0.0415560 * z; bl = 0.0556434 * x - 0.2040259 * y + 1.0572252 * z
    enc = lambda c: 12.92 * c if c <= 0.0031308 else 1.055 * max(c, 0) ** (1 / 2.4) - 0.055
    v = [enc(c) for c in (r, g, bl)]
    if any(c < -0.001 or c > 1.001 for c in v): return None
    return "#%02X%02X%02X" % tuple(round(min(max(c, 0), 1) * 255) for c in v)
