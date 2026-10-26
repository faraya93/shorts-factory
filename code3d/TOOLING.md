# code3d tooling notes (Blender 5.2.3 LTS, 2026-10-25)

## Build route
Scripts, not GUI: `blender -b --python <script> -- <args>` is the primary, deterministic, repeatable route
(spikes/blender_smoke.py shows the exact-colour recipe: node-based world/material, Standard view transform, sRGB->linear).

## Integrations installed and verified (Part 2 of the code3d setup; free tiers only)
- BlenderKit add-on v3.21.3 — installed as a Blender extension:
  `blender --command extension install-file -r user_default --enable <zip>` (zip from the GitHub release;
  the repo was renamed BlenderKit/Blendkit, so API calls need `curl -L`). The add-on registers headless.
  Anonymous search WORKS (https://www.blenderkit.com/api/v1/search/?query=asset_type:material+skin+is_free:true).
  Anonymous download WORKS: GET the file's downloadUrl with `?scene_uuid=<uuid4>` -> JSON with a signed `filePath`,
  then `curl` that URL (Python urllib gets a 403 on it; curl does not). No login, no API key.
- Poly Haven API (keyless): api.polyhaven.com/assets?t=hdris&c=studio, /info/<id>, /files/<id>. 96 studio HDRIs.
- ambientCG API (keyless): ambientcg.com/api/v2/full_json?q=<q>&type=Material&include=tagData,downloadData; zips at
  ambientcg.com/get?file=<Id>_2K-JPG.zip (each zip also contains a ready .blend material). No human-skin textures exist
  in CC0 libraries (the only "skin" hit is a leather); skin comes from the BlenderKit procedural SSS shader.
- Blender MCP: the package is now `mcp-for-blender` (blender-mcp is a compatibility wrapper); needs `uv`
  (brew install uv). Add-on: `uvx mcp-for-blender install-addon` (-> scripts/addons/blender_mcp.py). Claude Code:
  `claude mcp add blender -- uvx mcp-for-blender` (project-local config; shows "Connected"). Verified end to end through
  the real MCP server (scene query, HDRI import, test render) with spikes/mcp_verify_blender.py + mcp_verify_client.py.
  CAVEAT: the add-on refuses to start in `blender -b` by design (commands are drained by a main-thread timer), so the
  verification harness drove the add-on's own server code with a manual drain loop; the live-GUI path (open Blender,
  N panel -> MCP tab -> Start) and Claude Code's own client connection were not exercised. The MCP is for interactive
  GUI sessions; headless builds use scripts. Its `generate_3d` tool may call third-party services: not used.

## Part 2 cost (reported separately from any scene)
Wall clock 20:13 -> ~20:19 (about 6 min of the 45 min timebox); effort MEDIUM; fal spend $0. Course corrections: GitHub API
redirect (renamed repos), package rename, missing `uv`, urllib 403, the add-on's background-mode refusal.

## Reusable library built in v4 scene 2 (code3d/lib/) — reuse, never remodel
- `common.py`: exact-hex colours from the production's visual_identity (`identity`, `palette`, `linear`), render setup with
  DRAFT (540x960, 12 samples) and FINAL (1080x1920, 96 samples) modes, `studio_world` (HDRI lights the scene, the camera
  sees the exact spec backdrop via Light Path "Is Camera Ray"), `orbit` camera, area light, `principled`, `append_material`
  (appends a library material from code3d/assets without re-downloading), `smooth` easing, `render_frames`.
- `suture.py`: `box`, `skin_half` (peach skin layer over a red tissue block, bevelled), `wound_floor`, `curved_needle`
  (tapered arc tube whose origin is the circle centre, so one rotation about y drives it through the skin), `arc_points`,
  `resample`, `Thread` (thin tube whose polyline is rewritten every frame by a frame_change_pre handler).
- Scene recipe (code3d/scenes/scene_NN.py): reset scene -> render/world setup -> materials (library skin shader tinted to
  palette hexes) -> objects from the library -> a `frame_change_pre` handler that poses everything from time `t` ->
  stills for iteration (`stills=f1,f2`) or an animation (`frames=a-b`). Driver: `python factory/code3d_render.py
  <production> <scene> [--mode draft|final]` (slot frames come from the narration, the clip gets the exact frame count,
  the render is logged to costs.json).
- Material choices made for speed: the BlenderKit SSS Skin Shader (library) tinted to palette skin peach / shaded skin /
  tissue red; steel needle = Principled metallic in the palette's steel grey (the ambientCG Metal063 textures are
  pointless on a 0.1-unit tube and the tube has no UVs); thread = plain near-black Principled; HDRI = Poly Haven
  studio_small_08. Fabric079 was downloaded but not used.
- Observed speeds (Apple Silicon, EEVEE): ~0.11 s/frame draft, ~1.4 s/frame final for this scene.

## Library additions during the v4 batch (reuse these first)
- `stage.py`: `Stage(production, mode)` = materials (library skin shader tinted to the palette), studio world, camera, key
  light, and `stage.run(update, args, slot, name)` (stills for iteration or the animation). New scenes start here.
- `body.py`: `Forearm` (skin tube over a tissue core with an animated lens-shaped slit, welded seam).
- `props.py`: `load_tweezers` (BlenderKit Tweezers, grip opens/closes about the hinge, plastic retinted to the palette),
  `load_ant` (BlenderKit Ant (Rigged): jaws posed through the L.Nose / R.Nose bones; the ant faces -y), `jungle` (fern cards +
  green backdrop; the camera depth of field blurs it; cards cast no shadow).
- `suture.py`: `knot_polyline` (overhand/trefoil knot through a straight thread), plus the scene-2 objects.
- Gotchas found: the BlenderKit SSS skin shader blows out to white on thin shapes (use a plain Principled skin colour for
  lips/mounds); library assets bring their own colours (retint to the palette); a trefoil's end points sit at z = +/-0.9975
  and must be ramped to the skin; set `visible_shadow = False` on ground blocks and fern cards to keep shadows off the backdrop.
- Driver: `python factory/code3d_render.py <production> <scene> [--mode draft|final]` (slot frames from the narration).

## Cartoon style pass (code3d/lib/cartoon.py)
Opt-in per production: `"render_style": "cartoon"` in scenes.json. `cartoon.apply_if_requested(production, scene)` runs right
before rendering (hooked in `Stage.run` and in scene_02) and restyles by material NAME, so a new asset needs one line in
`restyle_materials` to land in the same register (unlisted materials keep their library look). Do not change the scene
scripts for a style change; change the pass. Measured: styling ~1 min, all six scenes ~20 min of final render.
