# Asset job: Elevator car in its shaft (elevator-car)

Started 2026-11-10.

## Brief
A closed elevator car hanging in a shaft: box, two sliding doors, a button strip and a floor display, two guide rails, landing doors every floor, hoist ropes. Moving parts: car root (falls, stops, sinks onto a buffer), ropes (grow in, are cut one by one), cut-away variant with a phone. Rigid and genuinely geometric, so the route is code primitives (CLAUDE.md "Asset library and hero routing").

## Sources searched (query, result, why taken or refused)
`factory/asset_library.py find elevator`: no match in the library. No library or generator search was run: the object is rigid and made of straight lines, the code-primitive route is the one the doctrine names for it, and the stool-unit precedent (code-primitive asset, `files.rig_module`) applies.

## Steps and visual checks
Built in `code3d/lib/asc_rig.py` (`shaft`, `Cab`, `Ropes`, `Buffer`, `phone`), looked at in EEVEE drafts from several angles and in Cycles gate stills. Colours come from `scenes.json` `hero_colours` and `support_colours`.

## Checks (QA, blind naming, fidelity)
- QA: no mesh to check (code primitives); recorded as pass, as for stool-unit.
- Blind naming, neutral Cycles still `job/stills/still-0015.png`, three isolated readers (`tools/blind_read.py`): "elevator car on guide rails" 85, "elevator car in a shaft (lift cabin on rails)" 85, "elevator car on guide rails in a shaft" 88. PASS.
- Fidelity: none (no reference photo).

## Wall time, spend ($0 expected), anything skipped
Spend $0. Built inside the 017 production session; the asset itself took under an hour. Not sealed for other poses: only the closed hanging car was read in the asset job; the cut-away car and the buffer are read per scene in 017.
