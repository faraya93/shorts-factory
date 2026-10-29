"""Hero rig for the clock video (reloj-coral): the motion work of a wall clock as a COMPOUND gear train, built from gear_rig's Gear class.
Stage 1: minute pinion A (10 teeth) -> B (30), 3:1. Stage 2: C (8 teeth, on B's shaft) -> D (32), 4:1. 3 x 4 = 12: D (hour hand) turns once per 12 turns of A (minute hand).
Both stages have the same centre distance (40 teeth * M / 2), so the layout closes exactly. A clock face (dial) with the two hands sits in front and lifts away to show the train.
Gears live in the XZ plane (camera looks along +y; nearer to the camera = smaller y); clockwise on screen = negative mesh angle."""
import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import gear_rig as gr  # noqa: E402

N_A, N_B, N_C, N_D = 10, 30, 8, 32
M = gr.M
DIST = (N_A + N_B) * M / 2                  # 3.2: also (N_C + N_D) * M / 2
PHI = (math.radians(55), math.radians(125))
PLANES = (1.86, 1.24)                       # stage 1 behind, stage 2 nearer the camera (C in front of B)
A_POS = (0.0, 0.0)
B_POS = (DIST * math.cos(PHI[0]), DIST * math.sin(PHI[0]))
D_POS = (B_POS[0] + DIST * math.cos(PHI[1]), B_POS[1] + DIST * math.sin(PHI[1]))
CENTRE = (0.9, 3.5)                       # framing centre of the train (x, z): the bounding box of the four gears
ZC = CENTRE[1]
DIAL_R = 3.9
MIN_LEN, HOUR_LEN = 3.2, 2.2


def mesh_angle(th_driver: float, phi: float, n_driver: int, n_driven: int) -> float:
    """Driven gear's mesh angle for a driver angle (tooth meets gap exactly; speed ratio n_driver / n_driven, reversed)."""
    return phi + math.pi - math.pi / n_driven - (n_driver / n_driven) * (th_driver - phi)


class Clock:
    def __init__(self, m, board=True):
        mats = gr.Train._materials(m)
        self.mats = mats
        fl = bpy.data.objects.get("floor")
        if fl:                                  # the shadow-catcher floor shows its horizon as a dark band at this camera distance; the dark plinth grounds the clock instead
            fl.hide_render = True
        self.A = gr.Gear("clk_A", N_A, A_POS, PLANES[0], mats["input"], marker=mats["marker"])
        self.B = gr.Gear("clk_B", N_B, B_POS, PLANES[0], mats["big"], marker=mats["marker"], holes=mats["ink"])
        self.C = gr.Gear("clk_C", N_C, B_POS, PLANES[1], mats["pinion"])
        self.D = gr.Gear("clk_D", N_D, D_POS, PLANES[1], mats["big"], marker=mats["marker"], holes=mats["ink"])
        self.gears = [self.A, self.B, self.C, self.D]
        cx, cz = CENTRE
        w, h = 9.4, 10.0
        yb = PLANES[0] + gr.THICK / 2 + 0.75
        zc = ZC
        self.board = tr.rbox("board", (w, 0.5, h), (cx, yb, zc), mats["taupe"], bevel=0.35) if board else None
        self.plinth = tr.rbox("plinth", (w + 1.0, 3.0, 1.2), (cx, yb - 1.1, zc - h / 2 - 0.6), mats["ink"], bevel=0.3)
        self.floor_z = zc - h / 2 - 1.2
        self.axle = [tr.cyl(f"axle{k}", 0.1, 1.9, (p[0], PLANES[0] - 0.1, p[1]), mats["ink"], axis="Y", verts=16) for k, p in enumerate((A_POS, B_POS, D_POS))]
        # clock face (dial) + hands, grouped so the dial can lift away; pivot = the centre of the dial
        self.dial = tr.empty("dial_root", (cx, 0.0, zc))
        y0 = PLANES[1] - 0.95
        tr.cyl("dial_disc", DIAL_R, 0.4, (0, y0, 0), mats["plate"], axis="Y", parent=self.dial, verts=96, bevel=0.06)
        for k in range(12):
            a = k * math.pi / 6
            big = k % 3 == 0
            tr.rbox(f"tick{k}", (0.2 if big else 0.1, 0.1, 0.55 if big else 0.32), (math.sin(a) * (DIAL_R - 0.55), y0 - 0.22, math.cos(a) * (DIAL_R - 0.55)),
                    mats["ink"], bevel=0.03, parent=self.dial, rot=(0, a, 0))
        self.hub = tr.cyl("hand_hub", 0.22, 0.5, (0, y0 - 0.5, 0), mats["ink"], axis="Y", parent=self.dial, verts=24, bevel=0.04)
        self.hour = tr.empty("hour_pivot", (0, y0 - 0.32, 0), parent=self.dial)
        tr.rbox("hour_hand", (0.34, 0.1, HOUR_LEN), (0, 0, HOUR_LEN / 2 - 0.2), mats["ink"], bevel=0.05, parent=self.hour)
        self.minute = tr.empty("minute_pivot", (0, y0 - 0.45, 0), parent=self.dial)
        tr.rbox("minute_hand", (0.2, 0.1, MIN_LEN), (0, 0, MIN_LEN / 2 - 0.2), mats["input"], bevel=0.04, parent=self.minute)
        self.dial_parts = [o for o in bpy.data.objects if o.parent is self.dial]

    def set_minute_turns(self, turns: float, phase: float = 0.0) -> None:
        """Drive the input by `turns` full minute-hand turns (clockwise on screen); gears and both hands follow the exact 12:1 train."""
        tha = -(2 * math.pi) * turns
        thb = mesh_angle(tha, PHI[0], N_A, N_B)
        thd = mesh_angle(thb, PHI[1], N_C, N_D)
        self.A.set_angle(tha); self.B.set_angle(thb); self.C.set_angle(thb); self.D.set_angle(thd)
        self.minute.rotation_euler = (0, -tha + phase, 0)
        self.hour.rotation_euler = (0, -(thd - thd0()) + phase / 12 + math.radians(300), 0)

    def dial_to(self, lift: float, hands: float = 1.0) -> None:
        """lift 0 = dial in front of the train, 1 = lifted clear above the frame; hands = scale of the two hands."""
        cx, zc = CENTRE
        self.dial.location = (cx, 0.0, zc + 12.0 * lift)
        self.dial.scale = (1e-4,) * 3 if lift >= 0.999 else (1.0, 1.0, 1.0)       # parked: fully out of every frame
        s = max(1e-4, hands)
        self.minute.scale = (s, s, s); self.hour.scale = (s, s, s)


    def set_gears(self, s: float) -> None:
        """Scale the whole train (and axles): 0 hides it behind the dial, 1 shows it."""
        s = max(1e-4, s)
        for g in self.gears:
            g.scale_all(s)
        for a in self.axle:
            a.scale = (s, s, s)
        if self.board:
            self.board.scale = (1.0, 1.0, 1.0)


def thd0() -> float:
    """D's mesh angle at zero input (hour-hand reference, so the hour hand starts at a fixed pose)."""
    return mesh_angle(mesh_angle(0.0, PHI[0], N_A, N_B), PHI[1], N_C, N_D)
