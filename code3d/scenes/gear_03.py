"""scene 3: the chain builds stage by stage on the spoken counts (una etapa, dos, tres, cuatro, cinco) while the camera pulls back from the first
pair to the whole chain; the last gear gets a marker pulse on 'mil veinticuatro veces más lento'. Slot 323 frames."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import gear_rig as gr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(323, floor_z=-5.1)
T = SLOT / c.FPS
A = gr.Train(m)
POP = [0.0, 2.86, 3.39, 3.95, 4.50]          # pair k appears at the word of its count; pair 0 is already there (scene 2 ended on it)
cx, cz = 1.9, 8.2


def update(scene_):
    t = scene_.frame_current / c.FPS
    for k, t0 in enumerate(POP):
        A.pop(k, 1.0 if k == 0 else tr.back((t - t0) / 0.45))
    A.set_input(2 * math.pi * 0.5 * t)
    u = c.smooth(1.8, 6.4, t)
    v = c.smooth(0, T, t)
    sx = (cx - 0.0) * u
    tr.look(stage, (sx, 0, 0.6 + (cz - 0.6) * u - 1.5 * u), 20.0 + 26.0 * u, 5.0 + 2.0 * u, -6.0 - 10.0 * v)


stage.run(update, args, SLOT, "gear-03")
