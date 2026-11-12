"""Block B5 proof 026-P2 (a still): the whole liner side-on and slightly high, shell at about 25% opacity, the walls opaque, funnels and bow kept opaque."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import titanic_rig as ti  # noqa: E402


S = sp.Shot(30, floor_z=-40.0)
m = ti.Mats(S)
ship = ti.Liner(S, m)
panels = ti.Panels(S, m)
lift = ti.lights(S, ti.LIGHT_K)
for shell in (m.hull, m.deck, m.white):                                     # the shell at 25%; the walls (bulkhead material) and the buff funnels stay opaque
    shell.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = 0.25
    shell.surface_render_method = "BLENDED"


def upd(t):
    ship.update(open=0.0, bulk=[1.0] * ti.NB, fill=[0.0] * ti.NC, funnel=1.0)
    ship.glow(None)
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (0.0, 0.0, 2.0), 320.0, 22.0, -4.0), (S.T, (0.0, 0.0, 2.0), 320.0, 22.0, -4.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
