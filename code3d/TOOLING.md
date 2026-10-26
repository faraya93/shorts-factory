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
