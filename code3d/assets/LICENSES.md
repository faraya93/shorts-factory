# code3d asset licences

Every asset downloaded into code3d/assets/ is logged here: name, source, licence, use. The assets themselves are
gitignored (media); this file is committed. Free tiers only — never subscribe or sign up for a paid plan
(BlenderKit Full etc.). Rules for sources not used yet: Meshy free-tier models are CC-BY and need an attribution
line in the video description; Tripo's free tier is non-commercial — never use it.

| Asset | Source | Licence | Used for |
|---|---|---|---|
| studio_small_08 (HDRI, 2k, `hdri/studio_small_08_2k.hdr`) — Sergej Majboroda | Poly Haven (polyhaven.com) | CC0 | studio lighting of all code3d scenes (tagged low contrast, softbox, infinity) |
| Metal063 (2K-JPG PBR, `materials/Metal063/`) | ambientCG (ambientcg.com) | CC0 | needle metal (tagged polished, glossy) |
| Fabric079 (2K-JPG PBR, `materials/Fabric079/`) | ambientCG | CC0 | suture thread (black fabric) — tested; may be swapped for plain black |
| SSS Skin Shader (`materials/blenderkit-sss-skin-shader.blend`; baseId 7cdb3a36-e89f-4c92-b8cd-e5cc5ab2c786) — Juan Mazzara | BlenderKit free plan (anonymous API download) | BlenderKit Royalty Free (`royalty_free`) | stylized subsurface skin: a procedural shader, so no realistic skin texture |

| Tweezers (`models/blenderkit-tweezers.blend`; baseId in the sidecar json) — Yahya Janani | BlenderKit free plan (anonymous API download) | BlenderKit Royalty Free (`royalty_free`) | scene 5: the tweezers that lift the stitch (plastic retinted to the palette's steel grey) |

| Ant (Rigged) (`models/blenderkit-ant-rigged.blend`) — Nik Kottmann | BlenderKit free plan | CC0 (`cc_zero`) | scene 6: the ant; jaws posed via the L.Nose / R.Nose bones |
| Tall Forest Fern (`models/blenderkit-tall-forest-fern.blend`) — Crazy0_0Cat | BlenderKit free plan | BlenderKit Royalty Free (`royalty_free`) | scene 6: blurred jungle fern cards. Also downloaded, not used: Fern Plant - Dense Foliage (Ibrohim Toxirov, royalty_free) |

Tools (not assets): BlenderKit add-on v3.21.3 (GPL-2.0-or-later), mcp-for-blender 1.30.0 (MIT), Blender 5.2.3 LTS (GPL).

| Metal012, Plastic010, Rubber004, Metal038 (2K-JPG PBR, `materials/<Id>/`) | ambientCG | CC0 | huincha-de-medir: blade steel, housing plastic, rubber grip, scratched steel |
| Measuring Tape 01 (`models/polyhaven-measuring-tape-01/`, 2k blend) — Kuutti Siitonen | Poly Haven | CC0 | downloaded and inspected, NOT used in renders: one baked mesh with one material (no separable blade, hook, shells or spring), so it cannot extend, cut away or explode. Kept as a proportion reference only. Also found and not downloaded (BlenderKit, royalty_free): "Tape measure" (Jp Mamuse), "25ft DeWALT Tape Measure" (Doug Teeples), same single-mesh limitation presumed. |
