"""dedos2 2 (orden): X-RAY of a real fingertip: translucent skin, an ivory bone, a branching vessel tree and a nerve inside; a signal runs down the nerve and the vessels tighten."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402
import finger_rig as fr  # noqa: E402

S = sp.Shot(246)
R, L = fr.R_DEFAULT, 16.0
skin = rk.wet_tissue("g_big", "#D79A74", sss=0.3, rough=0.35, coat=0.3)
skin.surface_render_method = "BLENDED"
nt_ = skin.node_tree                                                       # X-ray window: the skin is see-through near the tip and opaque up the shaft, so it is plainly a finger
b_ = next(n for n in nt_.nodes if n.type == "BSDF_PRINCIPLED")
geo_, sep_, mr_ = nt_.nodes.new("ShaderNodeNewGeometry"), nt_.nodes.new("ShaderNodeSeparateXYZ"), nt_.nodes.new("ShaderNodeMapRange")
tcn_ = nt_.nodes.new("ShaderNodeTexCoord")
nt_.links.new(tcn_.outputs["Object"], sep_.inputs["Vector"])
mr_.inputs["From Min"].default_value, mr_.inputs["From Max"].default_value = 8.5, 12.0
mr_.inputs["To Min"].default_value, mr_.inputs["To Max"].default_value = 0.22, 1.0
nt_.links.new(sep_.outputs["Z"], mr_.inputs["Value"])
nt_.links.new(mr_.outputs["Result"], b_.inputs["Alpha"])
F = fr.Fingertip(S, skin, "tip", L=L, loc=(0, 0, 0))
F.obj.visible_shadow = False
F.obj.rotation_euler = (0, 0, math.radians(-50))
bone_m = rk.wet_tissue("g_pin", "#E9DFC8", sss=0.1, rough=0.5, coat=0.0)
rb, zb = R * 0.33, R * 0.95
prof = [(0.0, zb)] + [(rb * math.sin(math.pi / 2 * k / 14), zb + rb * (1 - math.cos(math.pi / 2 * k / 14))) for k in range(1, 15)] + [(rb, L), (0.0, L)]
bone = rk.lathe("bone", prof, bone_m, seg=48, squash=(1.0, fr.FLAT))
bone.parent = F.obj
VM = rk.wet_tissue("g_mark", "#C0494E", sss=0.5, rough=0.3, coat=0.9)
t_ves, t_sq = S.t("vasos", default=5.5), S.t("aprietan", default=6.8)
trees = []
for sgn, seed in ((-1, 3), (1, 7), (-1, 11), (1, 5)):
    root = (sgn * 1.5, (0.5 if seed % 2 else -0.5), L - 0.4)
    rk.vessel_tree(S, f"v{sgn}{seed}", root, (sgn * 0.05, 0, -1), 6.0, 0.17, VM, depth=3, spread=0.5, seed=seed, rlim=(rb + 0.25, R - 0.4), zmin=0.8, grow=(t_ves - 4.0, t_ves - 2.4), out=trees)
for o, cu, _ in trees:
    o.parent = F.obj
base = [cu.bevel_depth for _, cu, _ in trees]
S.every_frame(lambda t: [setattr(cu, "bevel_depth", b * sp.interp([(0, 1.0), (t_sq - 0.6, 1.0), (t_sq + 1.0, 0.36)], t)) for (_, cu, _), b in zip(trees, base)])
NM = rk.wet_tissue("g_pin", "#F4E7A9", sss=0.1, rough=0.35, coat=0.5)
nx = -(rb + 0.3)
npts = [(nx, -0.2, L - 0.2), (nx - 0.1, -0.2, 11), (nx + 0.12, -0.2, 7.5), (nx - 0.05, -0.2, 4.2), (nx + 0.25, -0.2, 1.8), (nx + 0.9, -0.2, 1.0)]
no, _ = rk.tube(S, "nerve", npts, [0.1] * len(npts), NM, grow=(0.5, 2.5))
no.parent = F.obj
pulse = S.ball("pulse", S.accent, 0.3, npts[0], pop=(S.t("orden", default=4.4), 0.25))
pulse.parent = F.obj
t0 = S.t("orden", default=4.4)
S.move(pulse, [(t0, npts[0]), (t0 + 0.55, npts[1]), (t0 + 1.05, npts[2]), (t0 + 1.55, npts[3]), (t0 + 1.95, npts[4]), (t0 + 2.2, npts[5])])
S.gone(pulse, t0 + 2.2, 0.3)
S.box("plate", (30, 1.0, 36), (0, 6.0, 8.0), S.plate_mat(), bevel=0.5)
rk.softboxes(3.0, centre=(0, 0, 6), sides=False)
S.cam([(0, (0, 0, 9.0), 40, 8, -20), (4.0, (0, 0, 8.0), 31, 6, -12), (S.T, (0, 0, 6.0), 22, 4, 6)])
S.go()
