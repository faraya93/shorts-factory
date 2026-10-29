"""Hard-constraint table for the identity directions (owner round 2026-10-28). Run: python3 tools/constraints.py [tuned_bench.csv]
Thresholds (proposed, stated in docs/hard-constraints.md): C0 owner exclusions; C1 legibility; C2 hero separation over 36 colours;
C3 visibility vs white and black UIs; C4 cost under the tuned profile."""
import csv, json, math, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
sys.path.insert(0, __file__.rsplit("/", 2)[0] + "/factory")
import identity  # presets come from channels/umbrella-es.yaml (run with the project venv)
from palette_metrics import de2000, wcag, lab, lab2hex

FAM = {
 "objects": ["#F2BD12", "#CC2229", "#F2F1EE", "#151517", "#F28A1E", "#3FA34D", "#2E6FD6", "#E8719A", "#8A8F96", "#C8CBD0", "#7A4FBF", "#7B4A2A"],
 "body": ["#F2C9AE", "#8D5A3B", "#E58A99", "#A63C3C", "#EDE3D0", "#F3D675", "#CBD764", "#4A6FB5"],
 "numbers": ["#161618", "#F2F1EE", "#2F63D6", "#F5C04A", "#CC2229", "#8A8F96", "#3FA34D", "#26242E"],
 "what-if": ["#2E6FD6", "#3FA34D", "#B7B7BA", "#F5A623", "#D63B3B", "#161618", "#F4F4F6", "#2FA8B8"]}
T = dict(text=4.5, spoken=7.0, accent=3.0, error=3.0, hero_total=4, hero_family=2, ui=25.0, cost=5.0, min_L=30.0, celeste=25.0)
CELESTE = ["#9CCBEA", "#B9DCF0"]


def evaluate(d, cost=None):
    ends = (d["top"], d["bottom"])
    r = {}
    mid = lab2hex(*[(a + b) / 2 for a, b in zip(lab(d["top"]), lab(d["bottom"]))]) or d["top"]
    L = lab(mid)[0]
    a, b = lab(mid)[1], lab(mid)[2]
    hue = math.degrees(math.atan2(b, a)) % 360
    celeste = 190 <= hue <= 250 and L >= 60                  # light cyan-blue family = the Zack D look the owner excluded
    r["C0"] = (L >= T["min_L"] and not celeste, f"L*{L:.0f}, hue {hue:.0f}" + (" CELESTE" if celeste else ""))
    txt = min(wcag(d["ink"], e) for e in ends); sp = wcag(d["spoken_text"], d["spoken_box"])
    acc = min(wcag(d["accent"], e) for e in ends); err = min(wcag(d["error"], e) for e in ends)
    ok1 = txt >= T["text"] and sp >= T["spoken"] and acc >= T["accent"] and err >= T["error"]
    bad = [n for n, v, t in (("text", txt, T["text"]), ("spoken", sp, T["spoken"]), ("accent", acc, T["accent"]), ("error", err, T["error"])) if v < t]
    r["C1"] = (ok1, f"text {txt:.1f}, spoken {sp:.1f}, accent {acc:.1f}, error {err:.1f}" + (f" FAIL:{','.join(bad)}" if bad else ""))
    fam = {f: [h for h in hs if min(de2000(h, e) for e in ends) < 20] for f, hs in FAM.items()}
    tot = sum(len(v) for v in fam.values()); mx = max(len(v) for v in fam.values())
    r["C2"] = (tot <= T["hero_total"] and mx <= T["hero_family"], f"{tot} of 36 fail (max {mx}/family)")
    dw = min(de2000(e, "#FFFFFF") for e in ends); db = min(de2000(e, "#0C0C0E") for e in ends)
    r["C3"] = (dw >= T["ui"] and db >= T["ui"], f"white UI dE {dw:.0f}, black UI dE {db:.0f}")
    r["C4"] = (None if cost is None else cost <= T["cost"], "n/a" if cost is None else f"{cost:.2f} s/frame")
    return r


def load_cost(path):
    out = {}
    try:
        rows = list(csv.DictReader(open(path)))
    except FileNotFoundError:
        return out
    for row in rows:
        if row["scene"] in ("1", "3", "5"):
            out.setdefault(row["dir"], []).append(float(row["s_per_frame"]))
    return {k: sum(v) / len(v) for k, v in out.items() if len(v) == 3}


if __name__ == "__main__":
    D = {k: {**v, "top": v["top"], "bottom": v["bottom"]} for k, v in identity.presets().items() if v["lighting"] == "studio"}
    cost = load_cost(sys.argv[1]) if len(sys.argv) > 1 else {}
    names = [k for k in D if not k.startswith("_")]
    print("| direction | C0 exclusions | C1 legibility | C2 hero sep. | C3 UI visibility | C4 cost (tuned) | verdict |\n|---|---|---|---|---|---|---|")
    for k in names:
        r = evaluate(D[k], cost.get(k))
        cells = []
        for c in ("C0", "C1", "C2", "C3", "C4"):
            ok, info = r[c]; cells.append(("PASS" if ok else "FAIL" if ok is False else "n/a") + f" ({info})")
        allok = all(r[c][0] for c in r if r[c][0] is not None)
        print(f"| {D[k]['title']} | " + " | ".join(cells) + f" | {'SURVIVES' if allok else 'out'} |")
