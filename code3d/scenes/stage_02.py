"""v6-staged scene 2 (the hero): a giant chunky needle trailing a thick black cord laces the glossy boot criss-cross, one diagonal
at a time; every pull tightens the cord (anticipation: the needle draws back, then snaps) and pinches the flaps closer.
Slot 367 frames (12.23 s). The camera orbits and pushes in the whole time."""

import math
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import boot_world as bw  # noqa: E402
import common as c  # noqa: E402
import lace_world as lw  # noqa: E402
import shapes as sh  # noqa: E402
import suture as s  # noqa: E402

args, production, stage, m, SLOT = bw.begin(367)
T, ROWS, HX, HY = SLOT / c.FPS, bw.ROWS, 1.5, 4.7
LN, ZE, ZC = 3.4, 0.55, 0.85                                     # needle length; eyelet height; cord height above the panel
T0, DT, N_STEPS = 0.5, 1.38, 8

panel = bw.build_boot(m)
flap = {side: sh.rounded_bar(f"flap_{side}", HX, HY, 0.45, m.skin) for side in (-1, 1)}
tongue = sh.rounded_bar("tongue", 1.3, HY + 0.55, 0.2, m.red, loc=(0, 0.35, -0.32))
rings = {(side, i): sh.ring("eyelet", 0.3, 0.1, m.steel) for side in (-1, 1) for i in range(5)}
needle = sh.cone_needle("needle", Vector((0, 0, -LN / 2)), Vector((0, 0, LN / 2)), 0.5, 0.1, m.needle)
needle.rotation_mode = "QUATERNION"
eye = sh.ring("eye", 0.5, 0.15, m.needle)
SEQ = {0: [-1, 1, -1, 1, -1], 1: [1, -1, 1, -1, 1]}               # strand A / B: the side of each row's eyelet (criss-cross)
lace = [s.Thread(m.cord, points=190, thickness=0.24) for _ in (0, 1)]
stops = [sh.ellipsoid("stopper", 0.5, 0.5, 0.42, m.cord) for _ in (0, 1)]
bw.adopt(panel)


def eyelet_at(side, row, g):
    return Vector((side * (g(ROWS[row]) / 2 + 0.7), ROWS[row], ZE))


def lift(v, z=ZC):
    return Vector((v.x, v.y, z))


def step_geometry(j, g):
    """Where step j (strand j%2, diagonal j//2 -> j//2+1) starts, passes and ends, for the current eyelet positions."""
    strand, idx = j % 2, j // 2
    q0, q1 = eyelet_at(SEQ[strand][idx], idx, g), eyelet_at(SEQ[strand][idx + 1], idx + 1, g)
    u = Vector((q1.x - q0.x, q1.y - q0.y, 0)).normalized()
    start = q0 if idx == 0 else None
    if idx > 0:                                                   # re-grab the loose end left by the previous pull of this strand
        qm = eyelet_at(SEQ[strand][idx - 1], idx - 1, g)
        um = Vector((q0.x - qm.x, q0.y - qm.y, 0)).normalized()
        start = q0 + um * 1.1
    start = Vector((start.x, start.y, ZC))
    through = Vector((q1.x, q1.y, ZC)) + u * 1.0
    final = Vector((q1.x, q1.y, ZC)) + u * 1.1
    return dict(strand=strand, idx=idx, q0=lift(q0), q1=lift(q1), u=u, start=start, through=through, final=final)


def pose(j, tau, g, geo):
    """Eye position and needle direction of step j at local time tau (0..1) -> (eye, u, phase info)."""
    G = geo[j]
    u = (G["through"] - G["start"]).normalized()
    thread = c.smooth(0.17, 0.66, tau)
    snap = bw.back((tau - 0.78) / 0.22, 2.2)
    if tau < 0.78:
        E = G["start"].lerp(G["through"], thread) - u * (0.45 * c.smooth(0.66, 0.78, tau))
    else:
        E = (G["through"] - u * 0.45).lerp(G["final"], snap)
    return E, u


def update(scene_):
    t = scene_.frame_current / c.FPS
    taus = [(t - (T0 + j * DT)) / DT for j in range(N_STEPS)]
    pulls = [bw.back((tau - 0.78) / 0.22, 1.9) if tau > 0.78 else 0.0 for tau in taus]
    pinch = sum(min(p, 1.3) for p in pulls) / N_STEPS
    g0, k = 1.75 - 1.4 * pinch, 0.13 - 0.1 * pinch                # the V-shaped gap pinches closed, pull by pull
    g = lw.gap_fn(g0, k)
    phi = math.atan(k / 2)
    for side in (-1, 1):
        flap[side].location = (side * (g0 / 2 + HX), 0, 0)
        flap[side].rotation_euler.z = -side * phi
        for i in range(5):
            rings[(side, i)].location = lw.eyelet(side, ROWS[i], g, ZE)
    tongue.scale.x = ((g0 + abs(k) * HY) / 2 + 0.05) / 1.3
    geo = [step_geometry(j, g) for j in range(N_STEPS)]

    j_now = min(N_STEPS - 1, max(0, int((t - T0) // DT)))
    tau = taus[j_now]
    if t < T0:                                                    # the needle swings in from the left before the first stitch
        j_now, tau = 0, 0.0
    E, u = pose(j_now, max(0.0, tau), g, geo)
    hop = c.smooth(0.0, 0.17, tau) if j_now > 0 else c.smooth(-0.35, 0.17, (t - T0) / DT)
    if tau < 0.17 or t < T0:                                      # hop from where the last pull left the needle to the new start
        if j_now > 0:
            E0, u0 = pose(j_now - 1, 1.0, g, geo)
        else:
            E0, u0 = geo[0]["start"] + Vector((-7.0, -2.5, 2.5)), geo[0]["through"] - geo[0]["start"]
            u0 = u0.normalized()
        E = E0.lerp(E, hop) + Vector((0, 0, 1.2 * math.sin(math.pi * hop)))
        u = u0.lerp(u, hop).normalized()
    needle.location = E + u * (LN / 2 + 0.55) + Vector((0, 0, 0.1))
    needle.rotation_quaternion = u.to_track_quat("Z", "Y")
    eye.location = E + Vector((0, 0, 0.1))

    finished = [min(N_STEPS - 1, jj) for jj in range(N_STEPS) if taus[jj] >= 1.0]
    for strand, thread in enumerate(lace):
        done = [jj for jj in range(N_STEPS) if jj % 2 == strand and taus[jj] >= 1.0]
        cur = j_now if (j_now % 2 == strand and taus[j_now] < 1.0 and taus[j_now] >= 0.0) else None
        sides = SEQ[strand]
        base = lift(eyelet_at(sides[0], 0, g))
        path = [base]
        for jj in done:
            path.append(geo[jj]["q1"])
        if cur is not None:
            G = geo[cur]
            if path[-1] != G["q0"]:
                path.append(G["q0"])
            e_pt = E.copy()
            e_pt.z = ZC
            passed = (e_pt - G["start"]).dot(pose(cur, 1.0, g, geo)[1]) > (G["q1"] - G["start"]).dot(pose(cur, 1.0, g, geo)[1]) + 0.1
            if passed:
                path.append(G["q1"])
            path.append(e_pt)
        elif done:
            path.append(geo[done[-1]]["final"])
        else:
            path.append(base + Vector((0.0, -0.9, 0.0)) if strand else base + Vector((0.0, -0.9, 0.0)))
        slack = 0.35 * (1 - (pulls[cur] if cur is not None else 1.0)) if cur is not None else 0.0
        pts = []
        for a, b in zip(path, path[1:]):
            pts += lw.arch(a, b, 0.07 + slack)[:-1]
        thread.set(lw.chaikin(pts + [path[-1]], 1))
        stops[strand].location = lift(eyelet_at(sides[0], 0, g)) + Vector((0, 0, 0.05))

    p = c.smooth(0.0, T, t)
    focus = bw.to_world((0, -3.0 + 6.5 * c.smooth(T0, T0 + N_STEPS * DT, t), 0.5))
    bw.look(stage, bw.to_world((0, 0, 0)).lerp(focus, 0.45) + Vector((0, 0, 0.6)), 40.0 - 10.0 * p, 38 + 8 * p, -28 + 54 * p)


stage.run(update, args, SLOT, "stage-02")
