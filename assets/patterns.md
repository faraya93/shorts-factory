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
| Elevator car (017) | closed car, doors and button strip, on two rails past landing doors, medium-wide | shaft landings and rails | PASS (neutral 85/85/88; production still 90-92); the same car cropped tight, or with a wheel beside it, reads "wall cabinet / safe / vending machine" (30-45) | opaque |
| Elevator ropes (017) | six parallel ropes over a sheave, car at the foot of the frame | sheave, rails, car | PASS (60/80/80); at the moment the first rope is cut the readers named only the car (70/70/75) | opaque |
| Elevator safety brake (017) | wedge pair, caliper, G-clamp on the guide rail, tight or wide, with or without the car | rail, car underside | FAIL in 7 readings: "safe", "cabinet leg", "pants", "bracket" (25-62); a clamp bolted to a post is named clamp or bracket, never "brake", and the elevator context is lost once the frame is tight. Stays off screen; the beat is staged as the rails lighting up in the accent around the car's base (car reads 72-75 in a wide frame) | opaque |
| Elevator governor wheel (017) | spoked wheel with two weights rolling on a rail, beside the car | car | FAIL ("wall safe", "valve wheel", 35-45); stays off screen | opaque |
| Phone in a cut-away car (017) | phone slab floating in an open-front car, wide | car interior | Mixed (80/85/65): the third reader named the car; closer, larger phone and an interior lamp: 80/85/70 | opaque |
| Pit buffer (017) | coil spring around a rod, cap plate, car landing on it | rails, landings | FAIL while the car sits on it (55/55/55, named the car); PASS alone at the start of the scene (60/60/72, "coil spring on a post") | opaque |
| Skull (018) | library human-skull, side/three-quarter, ivory flat bone colour | none (phone beside it) | PASS (neutral 96/96/97; production still 92-95); tinted teal by the bone-conduction glow also PASS (96/96/97) | opaque |
| Phone (018) | chunky phone, ivory body, plate-coloured screen with record dot and teal bars, close-up | none | PASS (88/85/88); the same phone beside a skull is named only as an alternative (skull first) | opaque |
| Two skulls + small phone (018) | skulls facing each other, phone 62% scale between them, camera near | skulls | PASS 70/70/70; with the phone full size and dead centre, readers named the phone first (90/60/60, 55/80/85) | opaque |
| Sound rings (018) | thick teal tori seen edge-on and overlapping | skulls, phone | FAIL, read as "a teal key" (55/45/60); one slim ring or an arch seen at an oblique azimuth passes | opaque |
| Airliner exterior (019) | whole jet, three-quarter, wide, clouds | none | PASS (neutral 96/97/95; production still 95-97) | opaque |
| Airplane door (019) | door in a curved fuselage section, any distance, with or without a hand | oval windows | FAIL in 6 readings: "fuselage", "control panel", "light switch", "robot torso", "grey door" (15-92 but never the door as the subject); the same door read as an airliner's boarding door only inside a whole-plane frame, which names the plane | opaque |
| Airplane door (019) | door at the end of a cabin aisle, wider than its hole, accent stops, seat rows and bins around it, camera close | seats, bins, windows | PASS only at the closer framing (60/60/60 "airplane cabin door"); at a wider framing readers named the cabin (90/85/85) and the alias was missed | opaque |
| Airplane cabin (019) | side-on cut-away, passengers in profile | seats, windows | FAIL, "train carriage" (60/72/60); overhead bins and cloud windows did not fix it | opaque |
| Airplane cabin (019) | aisle view down five seat rows, bins, oval windows, passengers' heads over the seat backs | seats, bins | PASS (80/90/85, 85/80/85); a closed tube needs ceiling lamps in Cycles (the stage lights do not reach in) | opaque |
| Hand on a door handle (019) | sealed hand gripping a bar, 15-50 cm camera | door | FAIL in 4 readings: readers name "door handle" / "light switch", not the hand; stays off screen | opaque |
| Cars stacked (019) | five sealed sedans dropping onto a flat door on a teal pad | pad | PASS (60/60/60, then 90/85/90) | opaque |
| Car on a wet road (020) | sealed cartoon-car, side view, driver seated inside, ink storm cloud above | road, cloud | PASS (hero 60/90/75, scene 70/85/88); with the roof split off to a convertible 93/90/92 | opaque |
| Lightning bolt on a car (020) | thick accent zigzag from an ink cloud low over the car, car large | cloud, car | FAIL x2, readers name the car (96/85/92, 88/85/55) | opaque |
| Lightning bolt on a car (020) | cloud raised so the bolt is a tall picture, very wide frame, car small below | cloud, car | PASS (85/88/90); readers still name the car beside the bolt | opaque |
| Arc from a wheel to the road (020) | thin or thick arc on a tight tyre frame, with or without a glow pool | tyre, road | FAIL x2, "navy cartoon car", "teal puddle" (92/88/90, 93/92/92) | opaque |
| Arc from a wheel to the road (020) | whole bolt from the cloud plus the arc at the wheel, wide | cloud, car | PASS (90/90/90, "car struck by lightning") | opaque |
| Red bolt into an open car (020) | top-down push-in on the cabin | none | FAIL, "car with a red crash mark" (85/85/85) | opaque |
| Red bolt into an open car (020) | wide frame, cloud high, red bolt to the open cabin | cloud, car | PASS (85/85/92) | opaque |
| Toilet aerosol droplets | white beads in a green laser sheet; glossy streaked drops; blue drops on a white tile | toilet, tile | FAIL on every rung in 012: read as "white particle spray", "white foam", "blue paint splatter" (85/85/85, 88/85/85, 75/60/70) | |

