# Staging patterns that passed (or failed) blind naming

Written for production sessions: read this before staging an element, so the first attempt is one that already worked. Scores are reader confidences from each production's notes; recorded when the readers still had CLAUDE.md in context (see `docs/current/reports/reader-isolation/`), so treat them as upper bounds. Add a row after every gate round that taught something.

| Element | Staging | Context cue | Result | Render class |
|---|---|---|---|---|
| Ice | smooth slab | none | FAIL, read as mist (15/25) | |
| Ice | pile of real cubes | glass or pile | PASS (70-90) | nested transmission + volumes |
| Ice | cubes in a tray | blue ice tray | PASS (85/80; isolated re-read 90/90/90) | glass/water |
| Thermos | body alone | none | FAIL, "blue cylinder" (55/50) | |
| Thermos | body + side handle + red cup-cap | handle identifies it | PASS (72/70/55; isolated re-read 88-90 at a wide frame) | glass/water |
| Thermos cutaway | tight, dark frame | none | FAIL on dark tight frames (53-55); re-staged to frames 15/150 | |
| Coffee | plain mug | none | FAIL, "flat white coffee mug icon" (60/35) | |
| Coffee | coloured mug + steam | steam | PASS (80/80/80) | volumetric |
| Fingertip with vessels | fingertip alone | none | FAIL, read as a glass tube | |
| Finger x-ray | whole hand | hand identifies the finger | PASS (85/75) | SSS |
| Finger close-up | bare finger, no hand or nail | none | Isolated re-read low (35/35/90): "flesh-toned cylinder" | SSS |
| Bottle tower | stacked PET bottles, far camera | none | Isolated re-read low (40/55/55); keep a near bottle in frame | glass |
| Droplet spray | glowing round white beads in a laser sheet | toilet below | FAIL, "white particles" (85/85/85; right idea, undeclared word) | glass/water |
| Droplet spray | glossy streaked pale drops | toilet below | FAIL, read as foam (88/85/85): elongated pale drops look like suds | glass/water |
| Droplet spray | blue drops speckling a white tile | toilet below | FAIL, "blue paint splatter" (75/60/70): a flat white tile says paint | glass/water |
| Bowl water | shallow transmissive sheet over a pale floor, foam beads at the rim | seat and bowl | PASS (85/88/85); without the floor the refraction sees the unlit trap and goes dark | glass/water |
| Toilet brush | lifted, head above the rim, holder empty nearby | toilet | PASS (90/88/90); head hidden in the bowl gives only a stick | opaque |
| Toothbrushes | whole cup filling the frame | cup, taps, tile | PASS (96/96/95); the same cup small in a wide bathroom was missed | opaque |
| Poop (016) | smooth lumpy log alone | none | FAIL, "chocolate nugget / chicken nugget / potato" (35/35/35) | opaque |
| Poop (016) | matte coiled swirl, alone | none | PASS (85/85/80) | opaque |
| Poop (016) | coiled swirl on a kitchen scale beside the toilet | toilet | PASS (96/90/93, 92/92/92 after the ceramic recolour) | opaque |
| Poop heap (016) | hundreds of instanced swirls, toilet in frame | toilet | PASS (85-95); without the toilet in frame the same pile reads "chocolate pieces" (30/45/40) | opaque |
| Water tank (016) | opaque frame + one water block, tank fills the frame | none | PASS (80/80/80, 72/80/62); tank small beside a heap and toilet read 40/40/70; glass walls plus water render black (nested transmission) | glass/water (profile `transparent` needs the scene script listed in brand.yaml scene_types) |
| Horse (016) | library draft horse, side view, hair particles OFF | none | PASS (92/85/90); with tail and mane hair on, a Cycles frame took 19+ min | opaque |
| Suitcases (016) | two stacked, filling the frame | none | PASS (96/95/96); in a frame shared with a heap and toilet readers named only the heap (80/90/60) | opaque |
| Cars (016) | two cars on a see-saw, high plan view | none | PASS (70/72/70); keep a gap between the cars or they read as one wide car | opaque |
| Toilet aerosol droplets | white beads in a green laser sheet; glossy streaked drops; blue drops on a white tile | toilet, tile | FAIL on every rung in 012: read as "white particle spray", "white foam", "blue paint splatter" (85/85/85, 88/85/85, 75/60/70) | |

