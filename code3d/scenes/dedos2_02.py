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
nt_ = skin.node_tree                                                       # X-ray skin: see-through in the middle of the finger, solid at the silhouette (a Fresnel rim), so it reads as a finger of a hand, not a glass tube
b_ = next(n for n in nt_.nodes if n.type == "BSDF_PRINCIPLED")
fres = nt_.nodes.new("ShaderNodeFresnel")
fres.inputs["IOR"].default_value = 1.6
amp = nt_.nodes.new("ShaderNodeMath")
amp.operation = "MULTIPLY_ADD"
amp.inputs[1].default_value, amp.inputs[2].default_value = 2.6, 0.16
amp.use_clamp = True
nt_.links.new(fres.outputs[0], amp.inputs[0])
nt_.links.new(amp.outputs[0], b_.inputs["Alpha"])
solid = rk.wet_tissue("g_big", "#C98963", sss=0.3, rough=0.45, coat=0.2)
spin = (0, 0, math.radians(90))                                            # nails toward the camera (dorsal view): the first thing a reader sees is a hand
FX = (-2.35 * R, 0.0, 2.35 * R, 4.7 * R)
FL = (L - 1.8, L, L - 1.0, L - 5.0)
fingers = []
for i, (x, ln, m) in enumerate(zip(FX, FL, (solid, skin, solid, solid))):
    f = fr.Fingertip(S, m, f"f{i}", L=ln, loc=(x, 0, 0))
    f.obj.rotation_euler = spin
    fingers.append(f)
F = fingers[1]
F.obj.visible_shadow = False
bone_m = rk.wet_tissue("g_pin", "#E9DFC8", sss=0.1, rough=0.5, coat=0.0)
rb, zb = R * 0.33, R * 0.95
prof = [(0.0, zb)] + [(rb * math.sin(math.pi / 2 * k / 14), zb + rb * (1 - math.cos(math.pi / 2 * k / 14))) for k in range(1, 15)] + [(rb, L), (0.0, L)]
bone = rk.lathe("bone", prof, bone_m, seg=48, squash=(1.0, fr.FLAT))
bone.parent = F.obj
VM = rk.wet_tissue("g_mark", "#C0494E", sss=0.5, rough=0.3, coat=0.9)
t_ves, t_sq = S.t("vasos", default=5.5), S.t("aprietan", default=6.8)
trees = []
for sgn, seed in ((-1, 3), (1, 7), (-1, 11), (1, 5)):
    root = (sgn * 0.9, (0.5 if seed % 2 else -0.5), L - 0.4)
    rk.vessel_tree(S, f"v{sgn}{seed}", root, (sgn * 0.05, 0, -1), 6.0, 0.2, VM, depth=3, spread=0.5, seed=seed, rlim=(rb + 0.2, R - 0.5), zmin=0.8, grow=(t_ves - 4.0, t_ves - 2.4), out=trees)
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
palm = S.box("palm", (4.7 * R + 4.7 * R, 6.0, 10.0), (R * 1.2, 0.0, L + 3.0), solid, bevel=2.2)       # the back of the hand, so the fingers belong to something
rk.softboxes(3.0, centre=(0, 0, 6), sides=False)
S.cam([(0, (1.6, 0, 12.0), 74, 8, -8), (4.0, (0.4, 0, 9.0), 42, 6, 6), (S.T, (0, 0, 6.0), 30, 4, 14)])
S.go()
