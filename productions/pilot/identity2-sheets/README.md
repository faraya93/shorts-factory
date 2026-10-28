# Identity round 2 — channel background candidates (owner pick pending; nothing written to channels/ or CLAUDE.md yet)
Look = lighting/palette only; scene 3 choreography is tape_03's maths verbatim (code3d/scenes/tape_look2.py). Real hero colours everywhere.
Sheets (A | B2 | D | E, left to right): 1 wide tape mid-growth (t=2.33 s, counter 3.2 m climbing), 2 counter landed 3.4 m, 3 gold stress at the flatten (t=6.2 s), 4 red-and-white thermos (versatility; it sits in the caption band, a framing artefact of my quick scene, not of the looks).
Overlays/subtitles are the real Editor output (Montserrat, grey/white).

## s/frame (Cycles, Metal, 1080x1920, 8-frame benchmark minus ~4 s Blender startup; Look A's earlier measure was 4.9)
| look | settings | s/frame | vs A (4.4 measured today / 4.9 earlier) |
|---|---|---|---|
| A control | 256 spp | 4.4 | 1.0x |
| E dark teal | 256 spp | 4.3 | 1.0x |
| B2 warm | 256 spp, adaptive 0.02 | 12.6 | 2.9x  (over target) |
| B2 warm TUNED | 96 spp, adaptive 0.05, 4 bounces | 7.0 | 1.6x (stills look clean after denoise) |
| D celeste | 256 spp | 13.3 | 3.0x (over target) |
| D celeste TUNED | 96 spp, adaptive 0.05, 4 bounces | 6.9 | 1.6x |
Light studios cost ~3x at equal settings (big bright world + shadow-catcher floor = noisy); the tune gets both under 2x but is untested in motion (flicker risk from 96 spp is unknown).

## Four axes
Subtitle contrast (WCAG ratio, current word white / other words grey 150 vs backdrop): A 19 / 6.5; E ~15 / 5.1; B2 1.75 / 1.7; D 1.4 / 1.9. On B2 and D the text is legible ONLY thanks to the thick black outline (looks like a sticker, and the reference "white bold + grey" hierarchy is lost); dark backdrops keep the reference style intact. A dark-text variant would be needed for B2/D.
Versatility: yellow tape on tan B2 is the weakest (low hue separation); D makes yellow and red pop (complementary to blue); E and A flatter all colours; the gold stress glow reads strongest on A/E, weaker on D/B2.
Identity: A not ownable; E a distinct deep teal that keeps the gold accent doctrine; D is the closest to a Zack-D-style light-blue signature but contradicts the binding dark-stage doctrine (CLAUDE.md would need rewriting); B2 reads generic.
