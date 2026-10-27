# Reference style spec: the LOOK of the target channels

Source: docs/reference/ejemplo-1.MP4 (touchscreens, 91.2 s), ejemplo-2.MP4 (toilet paper and the bin, 68.5 s), ejemplo-3.MP4 (iPhone keyboard, 88.3 s).
All three: 720x1280, 30 fps, H.264 + AAC, 9:16. Video 1 and 3 are one channel (@resultaaquee), video 2 another (@ingenioculto); the look is shared.

## How this was made (and its limits)
- Frames at 2 per second (182 / 137 / 177 frames) plus the first frame of every shot (shot cuts found with ffmpeg scene detection at threshold 0.10; 14 / 10 / 10 shot starts), read as labelled contact sheets, plus three frames at full size. Pixel colours below were MEASURED (median of border pixels, or mean of saturated pixels), not eyeballed.
- Evidence is cited as [V1 12.0s] = video 1 at 12.0 s. Times are +-0.5 s (2 fps sampling).
- I cannot hear audio. Narration is read from the burned-in subtitles; voice, music and sound effects are NOT assessed here.
- Reference videos are gitignored (docs/reference/*.[mM][pP]4) and are not committed.

## 1. Colour

| Role | Measured value | Evidence |
|---|---|---|
| Background (void) | near-black, warm: #120F10 (V1, V3 border median), #151314 (V2) | [V1 1.5s] [V3 4.5s, 11.5s] [V2 25.0s] |
| Cross-section backdrop | dark navy #16202C with a dotted star/dust field | [V1 36.0s], [V1 0.0s] |
| Accent: "the active quantity" | gold/amber. Glow lines ~#F5C04A at their brightest (mean of thin lines #AB893F); filled zones #ECA432 | [V1 1.5s] arcs; [V3 11.5s] key zones |
| Passive objects | neutral greys: keys #2D2A2B, grid cells #51555A, bin ~#424144, toilet ceramic #DAD8D7 (lit side) | [V3 4.5s] [V1 20.0s] [V2 25.0s] |
| Natural hero materials | skin peach (fingertip ~#B9948D, lit), terracotta pipe #905932, glove blue-grey knit | [V1 36.0s] [V2 6.0s] [V1 14.0s] |
| Annotation / measurement | teal-cyan outlines and chips (frames around a cutaway, dashed pipe outline, "4 min" and "2001" chips) | [V2 12.0s, 36.5s, 39.0s, 55.0s] |
| Alert / negative | red: overflowing bar "10 x 44 = 440 px" | [V3 56.5-58.0s] |
| Biology / contamination | neon yellow-green particles | [V2 48.5-49.0s] |
| Text | white; spoken-now word bold white, rest grey (~55%) | all |

Rules:
1. Dark, low-key frame: >70% of every frame is near-black or dark grey. There is no pastel and no light stage anywhere (V1 0.0-91 s, V2 0-64 s, V3 0-84 s).
2. ONE warm accent colour carries meaning. Gold/amber = energy, charge, active zones, things being measured; everything passive is grey. Never decorative.
3. Teal is reserved for annotation graphics, red for an error or overflow, yellow-green for bacteria: each colour has exactly one meaning.
4. Colour is introduced at the moment the narration reaches it: the amber zone layer is dark grey until "lo que tocas" (V3 9.5-10.0 s); the finger glows gold only when it touches (V1 3.5 s, 11.5 s).

## 2. Model proportions and detail level
- Hero models are simplified and chunky, smooth-shaded, low-to-mid poly; detail is spent ONLY on the feature the fact is about:
  - Fingertip: rounded-rectangle capsule with a nail and concentric fingerprint ridges, no pores or hair [V1 31.0s, 36.0s]. The ridges are the only fine detail.
  - Glove hand: four equal capsule fingers plus a larger capsule thumb, a micro-grid knit texture, no joints or wrinkles [V1 14.0s, 16.0s]. Proportions are toy-like: fingers about 1/3 palm length.
  - Phone: accurate rounded rectangle with a Dynamic Island and a real, legible UI (call screen "Sofia", lock screen "7:42"), i.e. the UI is faithful while the hardware is minimal [V1 13.5s, 17.0s].
  - Toilet: smooth ceramic profile, no seams, slight visible faceting in the shading bands [V2 25.0s]; bin: plain cylinder with a pedal; toilet roll: bright cylinder with a perforated sheet; paper balls: lumpy icosahedron-like crumples [V2 0.0-3.0s].
  - Pipes: half-pipe terracotta with fine crack lines; water as a flat translucent blue-grey plane with a caustic pattern [V2 18.0-23.5s].
  - Keyboard: rounded-rect keys with sans letters, flat top, tiny bevel [V3 0.0-3.5s].
- Scale is exaggerated to make the mechanism legible: the thumb is larger than a key by 3.0 s [V3]; the pen tip is huge [V1 4.5-6.0s]; a single wire crossing fills the frame [V1 24.0s].
- Nothing is photoreal. There is no real skin texture and no blood. Real photographs appear ONLY as cards (person, book cover, patent page) [V3 58.5-63.5s].
- Whole scenes are built from 3-6 objects at most; the rest of the frame is empty void.

## 3. Materials
- Mostly matte/satin with a soft gradient and a faint specular; no outlines, no cel bands [V2 25.0s, V3 4.5s].
- Glass: clear tumbler with a soft white edge highlight and visible water level [V2 33.5s]. Metals: gold pen tip with a hard highlight [V1 4.0s].
- Energy is EMISSIVE: thin glowing tubes (arcs) with bloom that lights nearby geometry (the fingertip underside warms gold on contact) [V1 11.5s, 36.5-40.0s].
- Cross-sections are flat clean cuts: a layered strip (glass line, wires, RGB pixel dots in R-G-B order, grey slab) [V1 0.0-12.0s]; the underground tank is a box with a glass front plate and a cyan frame [V2 8.0-13.0s].
- Textures are procedural and tiny: knit weave, tile grid, water caustics, wood-grain cracks. No photo textures.

## 4. Lighting
- Low-key, one soft key light, soft shadows, dark ambient. A warm orange radial halo sits BEHIND the hero near the top of frame (V2 8.1s, 16.8s, 27.7s), giving a rim of warm light on the object's upper edge [V2 25.0s].
- Emissive accents are the second light source (gold glow on skin).
- Dark vignette toward the edges; no hard cast shadows on a visible floor except the faint dark floor tiles in V2 [V2 0.0-5.0s, 24-27 s].
- Floor/backdrop, when present, is dark tiles (V2) or an empty void with a hairline blueprint grid (V1 13.5s, V3 6.0s). It is never a bright stage.

## 5. Camera behaviour
- The camera is never static. Every shot has a slow dolly/push-in, drift, tilt or orbit; typical size change is 10-30% over the shot (V1 0.0 -> 8.5 s: the pixel strip grows about 1.5x; V2 0-5 s pans down following falling paper; V2 24-27 s slow push on the toilet).
- Three move families:
  1. PUSH-THROUGH (zoom into a surface to reach the mechanism): V1 17.0-19.0 s (phone glass -> wire grid), V1 23-24 s (grid -> single crossing), V2 29.5-30.5 s (toilet paper -> fibres), V3 0.0-3.5 s (low angle macro along keys).
  2. PULL-BACK reveal for multiplication or context: V1 28.5-29.5 s (one crossing -> hundreds), V2 58-60 s (one toilet+bin -> dozens), V3 44.5-49.5 s.
  3. ORBIT/TILT of a 3/4 diorama: V2 5-13 s (underground tank), V2 17.5-23.5 s (pipe in perspective), V3 8-12 s (tilted exploded keyboard).
- Between scenes the transition is a blur (rack-focus wipe) or a push-through, not a hard cut: V1 13.0 s, 30.5 s, 51.0 s, 57.0 s (blurred in-between frames).
- Side-on orthographic-looking cross-sections are used for mechanisms (V1 0-12 s, 31-40 s, 62-80 s); perspective 3/4 for objects (V2, V3).
- Depth of field is used as a transition tool (blurred frames), not as a constant effect.

## 5b. Hero-rig recurrence
- The same hero rig returns many times, re-lit with new data: V1 cross-section strip at 0, 3.5, 11.5, 31, 36, 52, 56, 62, 70, 75 s; the glove+phone scene at 13.5, 57.5, 59.5, 66, 73.5 s [V1]. Build ONE rig per video and revisit it.

## 6. Composition
- 9:16 with a reserved caption band: the top 15-28% of the frame holds subtitles and the handle bug; the hero sits in the lower 70% (V1 0.5 s: subtitle at y~19%, strip at y~55-65%).
- The hero is centred, 40-80% of frame width; negative space is large and dark [V2 25.0s].
- Graphic stacking inside a frame: object above, mechanism strip below, counters at the very bottom [V1 36.0-40.0 s: finger, arcs, pixel dots, numbers 100/81/63/85/100].
- Labels use short leader lines to the thing they name (hairline, 1-2 words) [V1 0.5-3.0 s, V3 1.5 s, 16.0 s].
- A tiny watermark (Instagram glyph + @handle) sits at the right under the caption band, then moves to left-mid at times [V1 0.5 s vs 11.0 s].

## 7. On-screen graphics and type
- Subtitles: sans-serif (Montserrat-like), 1-4 words per state, at most two lines; the current word is bold white, the other words grey; emphasised words get a rounded selection box with corner handles [V1 3.0s "dedo,", 19.0s "rejilla"; V3 6.0-8.0s]. Inline emoji after key nouns: lightning, drop, glove, thumb, target [V1 11.5s, 32.5s, 51.5s; V3 3.0s, 77.5s].
- Labels: ALL-CAPS, letter-spaced, tiny white (CRISTAL, CABLES, CARGA, FILA, COLUMNA, CRUCE, LANA, HILO CONDUCTOR) [V1].
- Numbers: monospace counters that change in place (100 -> 91/83/93 -> 81/62/84), pill chips in teal ("4 min", "2001"), ring-progress counters (5), lower-thirds with a source line ("111 lecturas por segundo, Apple iPhone X y posteriores") [V1 30.0 s, 36-40 s; V2 36.5 s, 39.0 s, 42.5 s].
- Source citations in 6-8 pt grey: "menos de 1 pF, Texas Instruments" [V1 77.5 s], "Patente de EE. UU. 8.232.973" [V3 63.0 s], corpus file name "es_50k.txt" [V3 25.0 s].
- End card, about 4 s: the last frame dims to ~25% brightness, an Instagram glyph animates through its gradient, and the @handle sits beneath [V1 87.0-91.2 s, V2 64.4-68.5 s, V3 84.2-88.3 s].

## 8. Differences from our current productions (record only; nothing built)
- Palette: references are near-black with one gold accent; our v4-v6 use the owner-approved lavender #E2D5F1 stage. This is a direct conflict to settle with the owner before any rebuild.
- Subject: references show a mechanism (cross-section, layers, particles); our v4-v6 show a single prop on a stage (boot, plate).
- Annotation: references carry labels, counters, chips and citations; ours carry none.
- Camera: both move constantly (v6 now matches this).

## Top 10 style rules
1. Dark, low-key frames (~#120F10 void); never a light stage. [V1 0-91 s, V2, V3]
2. One warm accent (gold/amber #F5C04A / #ECA432) means "the active quantity"; everything passive is grey; teal = annotation, red = error. [V1 1.5s, V3 11.5s, V2 12.0s, V3 57.0s]
3. Hero models are simplified and chunky; spend detail only on the feature the fact is about (fingerprint ridges, key letters, ions). [V1 36.0s, V3 4.5s]
4. Exaggerate scale so the mechanism is legible (thumb larger than a key; one wire crossing fills the frame). [V3 3.0s, V1 24.0s]
5. Energy and charge are emissive glowing tubes with bloom that light nearby objects. [V1 11.5s, 37.0s]
6. Cross-sections are flat clean cuts with a layer stack and tiny labelled parts; cutaways get a glass plate and a cyan frame. [V1 0.5s, V2 12.0s]
7. The camera never rests: slow push, drift or orbit in every shot; scene changes are push-throughs or blur wipes, not hard cuts. [V1 17-19 s, 13.0 s; V2 24-27 s]
8. Reserve the top ~25% of the frame for captions; centre the hero in the lower 70% with large dark negative space. [V1 0.5s, V2 25.0s]
9. Text system: 1-4 word subtitles with the spoken word bold and a selection box on key words, ALL-CAPS tiny labels with hairline leaders, monospace counters, teal chips, small source citations. [V1 3.0s, 19.0s, 30.0s, 77.5s]
10. Build ONE hero rig per video and revisit it re-lit with new data; finish with a dimmed end card, animated logo and handle (~4 s). [V1 rig at 10 returns; end card 87.0-91.2 s]
