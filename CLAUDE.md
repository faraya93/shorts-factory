# shorts-factory — project brief

## What this is
A factory that produces faceless YouTube Shorts in Spanish, engineered to
maximize views and retention. Every technical choice serves that goal. The
reference format is Zack D Films' stylized 3D "how it works" explainers —
we copy the mechanics, never scripts or footage: all scripts are original.

## Format doctrine (from channel research, Oct 2026)
- Vertical 9:16. Target 30–35 s per video (~110 words of narration). The
  reference's #1 video is ~31 s. Longer is a defect, not a bonus.
- Title: short question or "How X works", second person when natural,
  exactly ONE trailing emoji as an emotion label. No hashtags.
- Hook in the first 2 seconds. A new fact AND a new visual every 5–8 s.
  A twist in the last 3 s that loops back to the hook.
- Winning topic family: body/medical "how it works".
- Visual style: STYLIZED 3D animation, clearly CGI (Pixar-style explainer),
  NOT photorealistic, no real skin texture, no blood, no gore. Realistic
  graphic content risks YouTube age-restriction (kills reach and
  monetization) and disgust-skips; in this format the gross-out is
  conceptual, not visual. Our pilot rendered photorealistic — that is the
  anti-pattern to avoid.
- Scene prompts must spell out the ACTION (what moves, enters, exits,
  where): video models render nouns well and actions badly. Add an
  explicit "never ..." clause for the plausible wrong reading. Every
  scene prompt is prefixed by the production's identical style string.
- Narration: Spanish, channel voice es-CL-LorenzoNeural (edge-tts).
- Subtitles: burned in, short phrases (max ~4 words), bold white with a
  thick black outline, lower-third. Size/position are tuned constants in
  editor.py.

## Pipeline
Deterministic code wherever money or precision is involved; LLMs only
where judgment is involved.
- factory/producer.py — scenes.json → fal.ai clips. Estimate before
  spending; >US$1 requires the owner's explicit OK; US$3 hard cap per
  run; max 2 attempts per scene; scenes with a valid clip are skipped
  (runs are resumable, never pay twice); every generation is logged to
  the production's costs.json at the normal (non-promo) rate; one fixed
  seed per production; prompt_expansion always "disabled".
- factory/editor.py — narration per scene (edge-tts) sets the timeline;
  clips are trimmed, slowed (max 1.25x) or last-frame-frozen to fit;
  subtitles are rendered as PNG overlays (this machine's ffmpeg has no
  libass); outputs final.mp4 (1080x1920, 30 fps, H.264/AAC) + cover.jpg.
- Phases: A Producer ✓ · B Editor ✓ · C Scriptwriter (an LLM agent that
  writes scenes.json) · D Orchestrator · E Publisher (YouTube API,
  uploads private; the owner always makes the publish call).
- A production lives in productions/<channel>/<video-slug>/; scenes.json
  and costs.json are versioned, generated media is gitignored.

## House rules
- Never spend without showing the estimate first. The gates are rules,
  not suggestions.
- Verify fal.ai model IDs and prices against the current docs/schema
  before using them — never from memory.
- The fal key lives only in .env (gitignored). Never print, commit or
  echo it.
- Code, comments, filenames and JSON keys in English. Narration and
  titles in Spanish.
- Commit and push after each working phase, with a clear message. Never
  commit media files or .env.
- Report failures and semantically wrong renders plainly; never work
  around them silently.
- The owner approves topics, scripts, spend and publishing. You cannot
  hear audio or watch video: verify mechanically (format, durations,
  extracted frames) and never claim a render looks or sounds right
  beyond that.
