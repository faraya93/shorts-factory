# Publishing cadence decision (marketing lead; decided 2026-11-03)

**Decision: Mecanalia-es stays at ONE video per day per platform on the automated platforms (YouTube, Facebook, Instagram).** TikTok stays manual (owner decision) and is outside this decision.
This is the target cadence. It is not raised to 2 or 3 per day now, and no orchestrator change is requested.

## How it treats the 30-day test: kept pure
The test that began on 2026-11-01 (1 video/day) runs to its end (last post 2026-11-30) with NO cadence change. A mid-test change would mix two regimes in one dataset
and make the day-30 read-out unattributable. The earliest date to reconsider cadence is **2026-12-01**, after the test read-out.

## Reasoning
- **Evidence (weak, stated as such).** There is no controlled evidence on Shorts frequency. The sources are mostly tool vendors with unpublished methods; the common
  recommendation is about 1 per day, with 2-3 viable only for teams with strong production workflows, and "hook quality matters more than frequency"
  ([AIR Media-Tech](https://air.io/youtube-hacks/how-often-should-you-post-shorts-to-grow-faster), [fluxnote](https://fluxnote.io/guides/optimal-youtube-shorts-posting-frequency-2026)).
  The one large dataset (vidIQ, 10.2 M channels) covers long-form, not Shorts ([vidIQ](https://vidiq.com/blog/post/How-Often-Post-on-Youtube)). Nothing here justifies
  trading the test's integrity for a speculative gain.
- **Marketing lens.** Each Short is tested largely on its own merits, so more videos do mean more chances, but only if each keeps the doctrine (tangible-object hook, one
  mechanism, original script). Today's 7 productions are the whole catalogue; the format's quality bar, not volume, is the unproven variable. Learn first what one a day does.
- **Scriptwriter lens.** Script supply is the bottleneck for a higher cadence: each video needs a topic from the four families, a verifiable hook and a closing archetype, with no
  repeated mechanism. 1/day is 7 scripts a week; 2/day would force topics down the list into the weaker families the doctrine warns against.
- **Design lens.** Each video is a code3d production with a composition gate and a render of roughly an hour or more on one Mac. Rig reuse makes follow-on videos cheaper,
  but 14-21 builds a week would compress or skip the gate and design review.
- **Sustainable cadence (honest estimate).** The factory can sustain about 1 video per day, i.e. about 7 a week, working in batches (the 008-013 batch is that pattern). That is an
  inference from the build history (001-007 were rendered 2026-10-28 to 10-30, in bursts, with the first rig builds being the costly ones), not a measurement: the shared Claude Pro
  weekly quota is not visible from this repo, so 14-21 builds a week is unverified and I do not claim it.
- **Nothing to publish at a higher rate anyway.** 001-002 are live, 003-005 are queued through Nov 4, and 006-007 plus the 008-013 batch are the entire buffer.
  **Correction, 2026-11-04:** the batch actually built was 006-011, and the owner rejected all six (likeness failure, do not publish; `productions/mecanalia-es/INDEX.md`). There is no buffer.
- **Platform declaration.** The orchestrator's YouTube API audit declares at most 1 upload a day. Raising cadence would also mean updating that declaration, not just the queue rule.

## Conditions to revisit (all must hold, then the owner decides; any change needs the owner's separate go and an orchestrator change)
1. The 30-day test is complete (on or after 2026-12-01) and its read-out exists.
2. A buffer of at least 14 approved, unpublished productions beyond the queue, so a higher cadence does not drain it.
3. Production has held at least 10 videos per week for 3 consecutive weeks without exhausting the weekly quota.
4. Platform data supplied by the owner shows the videos hold viewers (retention) rather than only reach; without it, volume would scale an unmeasured format.
5. The orchestrator's one-per-day rule and the API audit declaration are updated deliberately.
If met, the first step is 2 per day on YouTube only, for 14 days, as its own labelled test. 3 per day is not on the table.
Revisit earlier only on a clear failure signal (for example a sharp, sustained drop in views across several consecutive videos) or if the owner changes the goal.

## What this project can and cannot see
- **Cannot see:** views, retention, subscribers or follower data on any platform. The factory repo holds no platform credentials and no analytics code, and I found no analytics
  reading in the orchestrator repo either (only upload and check tooling). Until such access exists, the agents see only what the owner pastes in.
- **Therefore:** no data-driven conclusion on cadence, topics or formats is possible yet. The owner is right to wait for a meaningful body of published videos: the full
  30-day test (about 30 videos per platform, each with at least a week of exposure) is the minimum, and even then it is one channel, one format, one month.
