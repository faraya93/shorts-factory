# Process and execution-time optimization: second opinion (2026-11-08)

Written for the owner, as an analysis to decide from. Nothing in the factory was changed: no code, doctrine or settings. This report is the only file added.
I cannot watch or hear video. Every number below is labelled:
- **measured**: taken from repo records (costs.json `render_seconds`, reports, notes, git timestamps);
- **inferred**: reasoned from measured numbers;
- **guessed**: no local evidence.

## 0. Where the time actually goes (measured)

Final-render wall time per production, summed from each production's `costs.json` (Cycles, SF_SAMPLES=64, 1080x1920, 30 fps):

| # | Content | Frames | Final render | Mean s/frame | Worst scene |
|---|---|---|---|---|---|
| 007 padlock | opaque | 1,481 | 1.20 h | 2.9 | 3.7 |
| 011 popcorn | opaque | 1,363 | 1.25 h | 3.3 | 4.9 |
| 006 fingers | water tray, SSS skin | 1,370 | 1.75 h | 4.6 | 6.0 |
| 010 heart/bottles | glass + water, no volumes | 1,349 | 1.75 h | 4.7 | 7.6 |
| 009 thermos | glass, coffee, steam volume | 1,399 | 2.18 h | 5.6 | 8.0 |
| **008 ice** | **glass + water + ice with a volumetric core** | **1,363** | **8.49 h** | **22.4** | **58.4 (scene 4, 3.5 h)** |

What this table shows:
1. **One class of scene is the outlier: nested transmission plus heterogeneous volumes.** Every 008 scene holds ice cubes whose cloudy core is a noise-driven Volume Scatter plus Volume Absorption (`real_kit.ice`). Those cubes sit inside refracting water inside glass, under the `transparent` profile (transmission 8, volume 2, max 14 bounces). Those scenes run 8–58 s/frame. Glass and water without volumes (010) run 3.8–7.6. That the volumetric core is the driver is **inferred** from this correlation, not isolated by a bench.
2. Videos without that class finish in 1.2–2.2 h, unattended and overnight-capable. **For them, render time is not the bottleneck; session time is.** Session time means gate rounds, blind-reader rounds, restaging and records.
3. **The 2026-11-06 resume day:** about 10.5 h from the first commit to the last. About 10.2 h of that was Blender final render: 006 1.75 h, 008 8.5 h (**measured** from costs.json and git timestamps, local time = UTC−5). The day was GPU-bound, not judgment-bound. Two early 008 attempts were also lost to GPU out-of-memory from parallel Blender jobs (**measured**, 008 notes.md).
4. **Gate rounds are where the session time goes (measured round counts):**
   - 006: scene 2 took four staging rounds; scene 5 took five.
   - 008: scene 2 took five reader rounds over four stagings.
   - 009: scene 2 took three separate sessions (11-05, 11-06, 11-07). The last one had to rename all seven scene records, because the hero's cap changed late.
   - Gate stills are cheap to render: 7–25 s each, **measured**, every-element report. The cost is the rounds themselves: staging edits, reader spawns, and records invalidated as a side effect.

So there are two separate levers: **(A)** make the transmission/volume class render 3–5x cheaper, and **(B)** cut the number of gate rounds and the records that go stale as a side effect. Everything below is sorted under one of them.

---

## 1. Evaluation of the six proposals

### Proposal 1: riskiest-first order + freeze point + per-scene hash manifest — **ADOPT, with a corrected premise**

**What the code already does (false premise, partly):** a per-scene freshness hash already exists. `gate.scene_fingerprint()` hashes, per scene: the scene script, the production's rig libraries, that scene's declared elements, the library assets and the hero colours. A change already re-reads only stale scenes. The real gaps are narrower:
- **Granularity.** `scene_fingerprint` hashes the whole production-level `rig_libs` list, not the libraries that scene actually imports. Editing `thermos_real.py` makes every scene stale, even a scene that never imports it. Comments count too: CLAUDE.md says editing a rig library "even a comment" invalidates records.
- **The hero record is bound to the whole production.** `check_hero()` compares `likeness.json` against `fingerprint(prod)`, which includes every gate scene script. A tweak to scene 7's camera makes the hero likeness stale and forces a hero re-read.
- **No freeze point.** Hero and shared elements are not gated before per-scene work starts. In 009 the hero (thermos) failed at 62/55 after the scenes had been built. The cup-cap redesign then touched every scene, and all seven records were renamed (**measured**, 009 notes.md).

**Changes:**
- (a) **Production order.** First the hero and every element shared by two or more scenes, gated in a neutral still and in one representative production still. Then the riskiest scene, ranked by the modellability audit and by having a bare liquid or a transparent element. Opaque, already-proven scenes come last.
- (b) **Freeze.** After (a) passes, the hero and shared elements are frozen. A later change to a frozen item is an explicit "unfreeze", logged in notes.md, and it re-reads every dependent scene.
- (c) **Dependency tracking.** Per-scene dependencies come from the scene script's actual imports (Python AST), hashed with comments and docstrings stripped.
- (d) **Hero record.** The hero likeness record is fingerprinted on the hero rig/asset plus the gate stills it was read from, not on every scene script.

**Expected saving:**
- On a 009-type late hero change: about 6 of 7 scene re-reads avoided, because the hero failure surfaces before the scenes exist (**inferred** from the 009 record).
- Typical production: 1–3 fewer reader rounds (**guessed**).
- (c) and (d) remove the comment-edit and camera-tweak cascades entirely (**inferred**). The repo has several manual carry-overs by pixel diff (006, 008, 009 notes): each one is a session spending time proving that nothing changed.

**Effect on quality:** none on what the viewer sees. The likeness bar is unchanged; every rendered still a reader saw still has to match.

**Implementation cost:** low-medium. About 40 lines in `gate.py` (AST import walk, normalized hash), one field for frozen elements in scenes.json, and tests.

**Risks:**
- An AST walk can miss a dynamic import (`importlib`, `exec`). Fail safe: if a script does anything the walk cannot resolve, fall back to the whole-production list.
- Freezing too early can lock in a hero that reads alone but fails in context. That is why (a) gates the hero in one production still, not only on a neutral stage.

**Improvement on the proposal:** also formalize the pixel-diff carry-over the sessions already do by hand (mean diff < 1e-4). If a stale scene's re-rendered stills match the stills the readers saw within a written threshold, the record carries over automatically, stamped "carried over". This is stricter evidence than an input hash (what the readers saw is what is rendered now), and it removes a manual step that sessions keep repeating.

### Proposal 2: cheaper transmission — **ADOPT AS A BENCH; one premise is false, one is already half-done**

| Item | Status in the repo | Verdict |
|---|---|---|
| Caustics off | **Already off.** `tape_rig.Stage._render_setup` sets `caustics_reflective = caustics_refractive = False` for every final. | **False premise:** no time to gain. |
| Transmission bounces 4 vs 8 | `transparent` profile uses 8; 0 renders a glass tray black (measured 2026-11-05); 4 was never tested. | Bench it. Risk: stacked cubes inside water inside glass need ~6+ interfaces, so 4 may turn the 008 cube piles black. A black interior is a likeness defect, not optical precision. Bench 4 / 6 / 8. |
| Fake glass for non-hero elements (Light Path) | **Half done.** `real_kit.noshadow()` already sets `visible_shadow = False` on glass, water and ice, which is the shadow-ray half. The indirect half (Transparent for diffuse/glossy rays hitting the glass) is not done. | Adopt for context glass only (tank walls, background bottles), never on an element under likeness test without a re-read. Saving: modest (**guessed** 10–25% on glass-heavy frames); most of the shadow-ray gain is already taken. |
| Principled Thin Wall | **Exists in Blender 5.2.3:** checked by listing the Principled BSDF inputs headless on this machine. Not used anywhere in `code3d/`. | Adopt for thin glass shells: tank walls, PET bottle walls (`bottle_real` models wall thickness = two interfaces per wall). One surface instead of two per wall cuts transmission depth. Saving **inferred** 15–35% on 010-type frames. Changes how the glass refracts, so affected elements need a re-read. |

**What the proposal misses: the biggest lever is the volumetric ice core, not the glass.** Options, in order of expected yield (all **inferred**, none measured):
1. **`volume_step_rate` 1.0 → 2–4** on the transparent profile. It is unset in the rigs (Blender default 1.0, read headless). Ray-march cost falls roughly in proportion. The core is a soft cloud, and coarser steps blur it slightly, which is optical precision only.
2. **`volume_bounces` 2 → 0 or 1** for the ice core: single scattering. The cloudy core still reads as cloudy, with slightly darker, flatter interiors.
3. **Replace the per-cube heterogeneous volume** with a surface approximation, for cubes that are not the element under test (the 36 background cubes of 008 scene 4). Two candidates: an inner shell with a translucent, noise-masked Principled, or subsurface on the cube itself. The lesson recorded in 008 is that *piles of real cubes* read as ice (70–90) and a smooth slab does not. Shape, frosting and pile are what the readers used; the exact cloudy volume is optical precision.
4. **Fewer volumetric objects in the frame:** 008 scene 4 draws 6×2×3 = 36 volume cubes. This is a staging choice (see §2.3).

Measured context for the gain: if 008's ice scenes fell to the 010 glass-and-water class (≤ 8 s/frame), 008's 8.5 h would become about 2.5–3 h (**inferred**, frames × 010-class s/frame).

**Effect on quality:** inside the owner's trade-off for every item, *if* a blind sheet shows no change in shape or readability. A thin-wall or fake-glass switch on a gated element changes its stills, and the record must go stale; the existing fingerprint does this only if the material lives in a hashed library, which it does (`real_kit.py`).

**Implementation cost:**
- One bench session of about 2 h. Frames 100–111 of 008 scene 4 and one 010 bottle-wall frame, a variant switch per option, s/frame and RMSE against a 1024-spp reference, blind sheets: the same method as `render-bench.md`.
- Result: a new named profile (e.g. `transparent_fast`) in brand.yaml. No rig code changes beyond material flags.

**Risks:** black interiors at low transmission depth; a fake-glass edge that no longer reads as glass (glass reads by its refraction at the rim). Mitigation: the bench includes a likeness re-read of one glass and one ice element on the winning variant before it becomes a profile.

### Proposal 3: four-tier gate ladder (Workbench → EEVEE → Cycles draft → Cycles final) — **ADOPT A NARROWER TWO-TIER VERSION; part of it is dangerous**

**Facts in the code:**
- Drafts are already EEVEE (`setup_render` "draft-full", 12 TAA samples) through `tools/draft_still.py`.
- The stills the blind readers see are rendered by `gate.py stills` as `mode=final`: **full-resolution Cycles at 48 samples**.
- The manual and CLAUDE.md "Render-time operations (a)" say gate rounds "judge cheap DRAFT stills". **The documentation and the code disagree.** The code renders reader stills in Cycles. That is arguably the right choice, but the documentation is wrong.

**Where the ladder is right:** staging problems should be caught before readers are spent. Reader rounds, not still renders, are the expensive unit: a round costs three subagent spawns, a session turn and a record.

**Where it is dangerous:**
- **Readers judging EEVEE stills for a Cycles final.** The likeness fingerprint hashes scripts, rigs, elements and colours, **not the render engine**. A record passed on EEVEE stills would stay "fresh" for a Cycles final that looks different. The render bench measured EEVEE at RMSE 12–14 levels from Cycles, with visible gloss and contact-shadow shifts. That is a hole in the hard gate.
- If any tier below Cycles feeds the likeness record, the engine and samples must enter the fingerprint, or the tier must be advisory only.

**Saving:** small in render time: stills are 7–25 s each (**measured**). The Workbench/EEVEE tiers save render seconds that barely exist.

**Recommended version:**
- **Tier 1, advisory, no readers:** EEVEE draft stills plus the first/middle/last contact sheet for the session's own staging and dynamism checks (as now).
- **Tier 2, decisive:** Cycles reader stills, **at half resolution (540×960) with the GPU denoiser**. Readers judge phone-size likeness, and a 540-wide still is a fair phone-size proxy. About 4x fewer pixels makes still renders ~3x faster (**inferred**).
- Tier 2 always uses the final engine. Transmission elements are never judged below Cycles (the proposal's own caveat, extended to all elements).
- Workbench: drop. It shows silhouettes only, and the model can check silhouettes from EEVEE at no extra cost.

### Proposal 4: external runner, fresh headless session per production, non-model verifier — **ADOPT LATER, after proposal 6's skill; pilot on one production**

**Premise check (verified on this machine, `claude --help`, Claude Code 2.1.308):**
- `--bare` reads only `ANTHROPIC_API_KEY` / `apiKeyHelper` ("OAuth and keychain are never read"), so the owner's constraint is correct.
- It is also stronger than stated: `--bare` skips hooks and CLAUDE.md auto-discovery. A bare run would ignore the doctrine and every enforcement hook even with a key. **Never use `--bare` here.**
- `claude -p` without `--bare` uses the subscription login.
- `--max-turns` is **not listed** in this version's help: verify before relying on it. A wall-clock `timeout` wrapper is a dependable cap.
- `--max-budget-usd` only means anything for API billing.

**What it buys:**
- A clean context per production. Today one long session carries 006, 008 and 009 history, and CLAUDE.md alone is 66 KB.
- An unattended sequence: production N+1's script stage while N's render runs.
- A verifier between units that is code, not opinion. It already exists in pieces: `gate.py check`, `publish_package.py check`, a grep of the chain log for `FAILED|INCOMPLETE|Traceback`, `ffprobe` duration and size.

**Saving:**
- Wall-clock: modest. Renders already run unattended (**inferred**).
- The real saving is **owner attention and Pro usage**: fresh contexts are smaller, so a usage window covers more work (**guessed**: Pro usage limits are not recorded in the repo).

**Risks:**
- (1) **The Pro usage cap.** A sequential run will hit the usage window mid-production. The runner must detect that exit and resume with `claude --resume <id>` after the reset, not restart and pay twice.
- (2) **Permissions in `-p`.** Use an allowlist in project settings (`--allowedTools` / settings), never `--dangerously-skip-permissions`. That flag would remove the guard on publishing and fal spend. fal spend has its own code gate, but publishing and account creation rely on the model obeying doctrine.
- (3) **Interactive asset jobs** (MCP for Blender, visual iteration) are the part least suited to headless runs. Pilot on an opaque, library-asset production first.
- (4) Readers are Agent-tool subagents, which `-p` sessions can spawn; verify on the pilot.

**Implementation cost:** low for the script (about 60 lines of shell plus the verifier). Medium for proving it on one production.

### Proposal 5: no parked sessions; renders detached with a completion signal; CPU prep during GPU renders — **ADOPT, with a hard boundary**

**Facts:**
- The chains already run detached (`nohup tools/queue_chain.sh`), and Claude Code's background Bash notifies on exit.
- The parked-session waste is real. On 11-06 the GPU was the critical path for about 10 h (**measured**). Part of the session's own work then collided with it (the OOM incident).

**What is safe in parallel with a Cycles final on this machine** (Apple unified memory: GPU and CPU share RAM):
- Allowed: script writing, beat sheets, narration (edge-tts, network), subtitle and overlay work, asset searches and downloads, notes, the idea bank.
- **Not allowed:** any Blender process: headless stills, `draft_still.py`, `gate.py stills/run`, and **MCP for Blender with a live GUI**, which holds GPU memory too. Also not allowed: heavy ffmpeg encodes (CPU contention slows the render's scene sync and denoise only slightly, but memory matters more).

**Saving:**
- Per production after the first in a run, roughly the length of its script/beat-sheet/narration stage, overlapped instead of serial (**guessed**: 30–90 min).
- Bigger for transmission productions, whose renders are long enough to hide a whole script stage.

**Risk:** the session's natural next step after a script is gate stills, which need Blender. Without enforcement (proposal 6) the parallelism collapses back into the OOM incident.

**Implementation cost:** none beyond the lock in proposal 6 and a rule in the skill.

### Proposal 6: hooks to enforce one Blender job at a time + a reusable /produce skill — **ADOPT BOTH, but put the lock in code, not only in a hook**

**Enforcement gaps found in the code:**
- `tools/queue_chain.sh` waits on `pgrep -f "tools/chain_render.sh"`. That pattern **does not match `tools/chain_render2.sh`**, the script `tools/render_queue.sh` runs. The two queues do not see each other.
- Neither queue sees `gate.py`, `draft_still.py`, `final_still.sh` or the MCP Blender GUI.
- A Claude Code hook only sees *the model's* tool calls. It cannot stop a detached shell script from launching Blender while another is running.

**Recommended design:**
- **One GPU lock in code.** A single launcher (e.g. `tools/blender_run.py`) that every Blender entry point calls: `code3d_render.py`, `gate.py`, `draft_still.py`, the stills tools and the chains. It holds an exclusive file lock (Python `fcntl.flock`, since macOS ships no `flock` binary) for the whole process life, and it adds `caffeinate -dimsu`, so the standing caffeinate rule moves into the same place.
  - A second job waits, or refuses with a clear message.
  - The MCP Blender GUI cannot take the lock. The launcher therefore refuses a headless render while a GUI Blender process is open with GPU memory, unless an explicit override is given. The asset-job operating model must say "close or idle the GUI before a final".
- **Hook as a backstop.** A PreToolUse hook on Bash that denies a command containing `blender ` unless it goes through the launcher. It enforces the route; the lock enforces the rule.
- **/produce skill.** A project skill with the standard sequence:
  - draw from the bank;
  - script and flatness check;
  - riskiest-first order and freeze point (proposal 1);
  - render-cost class (§2.3);
  - beat sheet and lens approval;
  - tier-2 gate;
  - queue the final;
  - prep the next production in parallel;
  - verifier;
  - report.

  It should **link to** the CLAUDE.md sections, not copy them: copied doctrine drifts.

**Saving:**
- Lost renders from OOM: the 11-06 incident cost two 008 attempts (**measured** count; duration not recorded).
- Fewer session minutes re-deriving the sequence each time (**guessed**).

**Implementation cost:** low (launcher ~50 lines, hook ~15 lines, skill ~1 page).

**Risk:** a stale lock after a crash. Use flock semantics (released when the process dies), not a lock file that has to be deleted.

---

## 2. Additions nobody proposed

### 2.1 `chain_render.sh` re-renders the gate on every launch — **fix (measured bug)**
`tools/chain_render.sh` runs `gate.py run` unconditionally. `chain_render2.sh` runs `gate.py check || gate.py run`. `queue_chain.sh`, the tool the doctrine names, calls `chain_render.sh`, so every queued final first re-renders all masked gate stills in Cycles at 48 spp, even when the record is fresh.
- Saving: minutes per production for opaque videos; more on transparent ones, where 48-spp stills of a 58 s/frame scene cost about a minute each (**inferred**).
- Cleanliness: two chain scripts and two queue scripts that diverge. Merge them into one chain and one queue.

### 2.2 Final render at reduced resolution, upscaled in the editor — **bench, likely adopt**
Render Cycles at 75% linear (810×1440, 56% of the pixels) and let the editor scale to 1080×1920 (Lanczos) before subtitles, which stay full-resolution overlays.
- Cycles time scales close to pixel count once per-frame overhead is small (persistent data is on).
- **Inferred saving: 30–40% on every final**, about 0.5 h on a 1.5 h video and about 3 h on an 008.
- Quality: some softness on fine edges. Shape, silhouette and readability are unchanged; YouTube recompresses Shorts heavily anyway. This is optical precision under the owner's trade-off.
- Risk: thin structures (spring coils, the tower of 960 bottles) may shimmer. Bench on 010 scene 5 (tower) and the tape spring with a blind sheet, as in `render-bench.md`.
- Readers keep seeing Cycles stills; the likeness of the element is unchanged by output resolution. To be strict, the resolution can enter the fingerprint.

### 2.3 Render-cost class in the beat sheet, priced before the scene is built — **adopt**
The house rules already require an estimate table; this makes it predictive. Each scene in the beat sheet gets a cost class from the **measured** s/frame of comparable scenes:
- opaque: 2.5–5 s/frame;
- glass/water/SSS: 4–8;
- nested transmission plus volumes: 15–60.

A scene predicted above ~15 s/frame gets a **cost restage on paper** before modelling. Examples: fewer volumetric objects (12 cubes instead of 36), volumes only on the cubes near the camera, the glass tank replaced by a context cue that is not transmissive. This is ladder rung 1 used for cost instead of likeness; it keeps the narration and the beat.
- **Inferred saving on an 008-class video: several hours.**
- Quality: likeness is unchanged, because the restaged scene still passes the full gate.

### 2.4 One render for both gate stills — **adopt when touching gate.py**
`gate.py run` (masked, for the colour gate) and `gate.py stills` (unmasked, for readers) render the same frames twice in Cycles, in separate Blender processes. Rendering once with an object-index or Cryptomatte pass and deriving the mask from it halves still renders and Blender start-ups.
- Saving: small (minutes per production, **inferred**), but it removes the risk of the two still sets drifting apart.
- Risk: the composition gate's mask classifier must read the pass correctly. Validate it against existing records first.

### 2.5 A catalogue of staging patterns that passed — **adopt (cheap, cuts reader rounds)**
The asset library stores objects. The lessons that cut gate rounds are about *staging* and today sit scattered in notes:
- a smooth ice slab reads as mist (15/25), piles of real cubes read as ice (70–90), an ice tray made the ice read (85/80);
- the handle is what makes a thermos read; without it, "blue cylinder" (55/50);
- coffee in a plain mug reads as a "flat white coffee mug icon" (60/35); with steam and a coloured mug it scored 80/80/80;
- a vessel-filled fingertip on its own reads as a glass tube, while an x-ray finger on a hand reads (85/75).

A small `assets/patterns.md` (element, staging, context cue, reader scores, s/frame) would make riskiest-first concrete. The first staging tried is then the one that already passed.
- **Inferred:** removes 1–3 rounds wherever a pattern is reused.

### 2.6 Lower adaptive-sampling precision on the transparent profile — **bench with 2.2**
The tuned bench found the adaptive threshold to be the second-largest lever: 0.02 → 0.04 = 1.7 s/frame saved (**measured**, gear scene). Try 0.06–0.08 on transparent scenes only, where denoised noise on refractive surfaces is optical precision. **Inferred** 10–25%.

### 2.7 EEVEE finals for fully opaque productions — **test once, do not assume**
On the measured bench EEVEE was 2.3x faster than tuned Cycles but differed visibly: gloss sweeps and contact-shadow emulation (RMSE 12–14 levels). Under the owner's new trade-off, the gloss difference is negotiable. The contact-shadow band artefact is a defect, not precision.
- Opaque videos only take 1.2–1.25 h (**measured**), so the ceiling is about 0.7 h per opaque video.
- Worth one blind test on 007 or 011. Not worth it before 2.2, which gives a similar gain with no change in look.

### 2.8 Reader prompts kept clean of doctrine — **verify, this concerns validity as well as time**
CLAUDE.md is 66 KB and names this catalogue's subjects (hand, thermos, ice, coffee, heart, bottles). If the reader subagents inherit CLAUDE.md, two things follow:
- (1) **The "blind" readers are primed.** That inflates passes, which is a gate-validity risk, not a time saving.
- (2) Each reader carries tens of thousands of tokens of context, which matters on a Pro usage cap.

I did not verify whether the readers in past runs received it. Check this once. If they do, give readers a dedicated minimal agent definition: image-read tool only, no project memory.

### 2.9 Session context diet — **recommend, owner/lens decision**
Every session turn carries CLAUDE.md (66 KB, many sections superseded and then re-read "through" newer ones). A short core file (rules in force, one line each, with links) plus the specs, read on demand, would cut per-turn context sharply.
- On Pro, more work fits in a usage window, which is wall-clock time when the window, not the GPU, is the limit (**guessed**: no usage data in the repo).
- This changes doctrine layout only, not doctrine content. It needs a lens decision.

### 2.10 Considered and rejected
- **Frame interpolation (render 15 fps, synthesize 30):** artefacts on refraction and edges, and the camera always moves. It would damage readability, which is the protected quality.
- **Cycles path guiding:** it is CPU-only in Cycles, and the finals run on the Metal GPU (from my own knowledge, not verified on this machine).
- **CPU+GPU hybrid devices:** on Apple Silicon, unified memory and an already-busy CPU make the gain doubtful (**guessed**). Not worth a bench before 2.2 and 2.6.
- **Fast GI:** 4% measured; not worth the interior-scene risk.

---

## 3. Flags: wrong, dangerous or false-premise items

1. **Caustics off (proposal 2) is already the case** in every final (`tape_rig.Stage._render_setup`). No saving to claim.
2. **Light-Path fake glass for shadows is already done** by `noshadow()`. Only the indirect-ray half is new.
3. **The per-scene hash manifest (proposal 1) largely exists** (`scene_fingerprint`). The real work is narrower: per-scene imports, comment-stripped hashing, and decoupling the hero record.
4. **Readers on EEVEE (or Workbench) stills feeding the likeness record would open a hole in the hard gate:** the fingerprint does not cover the render engine. Advisory only, or the engine joins the fingerprint.
5. **`--bare` would also drop hooks and CLAUDE.md**, not just the subscription login. It would run the factory without its doctrine.
6. **A hook alone cannot enforce "one Blender job at a time":** detached scripts never pass through it. The lock must be in the launcher code.
7. **Doc–code mismatch:** the doctrine says gate rounds judge "cheap DRAFT stills"; `gate.py stills` renders full-resolution Cycles at 48 spp. Fix the documentation or the tier; do not leave both.
8. **Doctrine conflict to settle:** asset jobs are "interactive with Blender open through MCP", and Blender jobs run "strictly one at a time". A GUI Blender holding GPU memory during a queued final is exactly the OOM setup. The launcher in proposal 6 needs an explicit rule for the GUI.
9. **Any round-saving scheme must count every reading.** Reader variance is large: 85 vs 35 on the same still (**measured**, resume report). "Re-roll a reader until it passes" would game the gate. Short-circuiting a round after one reader under 45 is legitimate; discarding a reading is not.

---

## 4. Recommendation

**Execute, in this order:**

| Step | What | Why first | Cost | Expected saving (basis) |
|---|---|---|---|---|
| 1 | GPU lock in one launcher (+ caffeinate there), hook backstop, merged chain/queue scripts with check-first gate (P6 + §2.1) | Prevents lost renders and makes P5 safe; fixes a measured bug | ~half a session | OOM losses avoided (measured incident); minutes per queue (inferred) |
| 2 | Transparent bench on 008 s4 and 010 s5 frames: volume step rate, volume bounces, transmission 4/6/8, Thin Wall, indirect fake glass, adaptive 0.06–0.08, 75% resolution (P2 + §2.2 + §2.6) | The single largest lever; one session decides it | ~2 h incl. renders | 008-class 8.5 h → ~2.5–3 h; every final −30–40% if 75% passes (inferred) |
| 3 | Gate changes: per-scene import-based fingerprint, comment-stripped hashing, hero record decoupled, automatic pixel-diff carry-over, half-resolution Cycles reader stills, single render for both still sets (P1 c–d, P3 two-tier, §2.4) | Cuts stale cascades and the cost of each still | ~1 session + tests | rounds and re-reads avoided (inferred, from 006/008/009 records) |
| 4 | /produce skill with riskiest-first, freeze point, render-cost class, staging-pattern catalogue, parallel CPU prep (P1 a–b, P5, P6, §2.3, §2.5) | Turns the above into the default sequence | ~half a session | 1–3 fewer reader rounds per production (guessed); 30–90 min overlap per production (guessed) |
| 5 | Verify the reader context (§2.8) | Gate validity | minutes | n/a (validity) |
| 6 | External runner pilot on one opaque, library-asset production (P4) | Only worth it once 1–4 make a run predictable | ~1 session | owner attention and Pro usage (guessed) |

**Defer:** the EEVEE-finals test for opaque productions (§2.7), until 2.2 is measured. The CLAUDE.md context diet (§2.9), which is a lens decision with its own record.

**Drop:** the Workbench tier; reader decisions on any non-Cycles still; frame interpolation; path guiding; CPU+GPU hybrid devices; Fast GI.

**Order of magnitude, if steps 1–4 land as inferred:** an opaque video goes from about 1.2–1.75 h to about 0.8–1.1 h of render. A transmission-heavy video goes from 8.5 h to about 2–3 h. Session time falls by the gate rounds that riskiest-first and the pattern catalogue avoid. Of these, only the render figures have a measured baseline; the session-time saving is a judgement until a production is run under the new sequence and timed against this report.

**Owner-only items:** none. Every step above is creative or technical and falls under the lenses' standing authority. None of it spends money, publishes, or creates an account.
