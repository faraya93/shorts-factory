"""imanes scene 4 (cadena-de-clips): each clip becomes a temporary magnet and holds the next; remove the magnet and almost all of the chain falls."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(316, floor_z=-1.2)
T = SLOT / c.FPS
mats = mr.setup()
SC, STEP = 1.5, 2.2                       # clip scale, vertical pitch of the chain
mag = mr.Magnet("M", mats, thick=1.5)
mag.root.scale = (0.8, 0.8, 0.8)
MZ = 10.6
stand = mr.stand(mats, 5.2, MZ + 1.2, 0.0, 0.0)
clips = [mr.make_clip(f"clip{i}", mats["steel"], wire=0.08, scale=SC) for i in range(4)]
caps = []
for i, k in enumerate(clips):
    top = tr.cyl(f"cap_n{i}", 0.2, 0.2, (0.0, -0.25, 1.4), mats["n"], axis="Y", parent=k, verts=24)
    bot = tr.cyl(f"cap_s{i}", 0.2, 0.2, (0.0, -0.25, -1.4), mats["s"], axis="Y", parent=k, verts=24)
    caps.append((top, bot))
FLOOR = [(-4.6, 0.2), (-3.2, 0.2), (-1.8, 0.2), (-0.4, 0.2)]          # where the clips wait (lying flat on the plinth)
HOLD = [MZ - 2.1 - i * STEP for i in range(4)]                  # z of each held clip
ATT = [1.3, 3.55, 4.95, 5.55]                                         # attach start times (spoken: clip / un clip sostiene / ese a otro / más)
FALL = [8.1, 8.3, 8.5]                                                # clips 2..4 fall (clip 1 stays on the magnet: "casi toda")
LAND = [(1.6, 0.1), (-1.0, 0.1), (3.0, 0.1)]


def update(scene_):
    t = scene_.frame_current / c.FPS
    away = c.smooth(6.9, 7.9, t)
    mag.place(0.0 + 6.5 * away, MZ)
    stand.location = (5.2 + 6.5 * away, 0.0, 0.0)
    for i, k in enumerate(clips):
        a = c.smooth(ATT[i], ATT[i] + 0.7, t)
        hx = 0.0 + 6.5 * away if i == 0 else 0.0
        x0, z0 = FLOOR[i]
        x = mr.lerp(x0, hx if i == 0 else 0.0, a)
        z = mr.lerp(z0, HOLD[i], a)
        flat = 1.0 - a                                                  # lying flat (rotated about x) until it rises
        rot = (math.pi / 2 * flat, 0.0, 0.0)
        if i > 0:
            f = c.smooth(FALL[i - 1], FALL[i - 1] + 0.75, t) if t >= FALL[i - 1] else 0.0
            if f > 0:
                f2 = f * f
                x = mr.lerp(0.0, LAND[i - 1][0], f2)
                z = mr.lerp(HOLD[i], LAND[i - 1][1], f2)
                rot = (math.pi / 2 * f2, 0.0, 0.4 * f2)
        k.location = (x, 0.0, z)
        k.rotation_euler = rot
        n_cap, s_cap = caps[i]
        on = 1.0 if (t > ATT[i] + 0.9 and (i == 0 or t < FALL[i - 1])) else 0.0
        if i == 0:
            on = 1.0 if t > 2.1 else 0.0
        n_cap.scale = s_cap.scale = (max(1e-4, on),) * 3
    u = c.smooth(0, T, t)
    tr.look(stage, (0.8, 0, 6.4), 23.0 + 2.0 * u, 8.0, -4.0 + 8.0 * u)

stage.run(update, args, SLOT, "magnet-04")
