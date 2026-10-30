# por-que-no-nos-gusta-lo-mismo: why people do not taste food the same way (Coral) — production notes, 2026-10-30

## Publish package (Spanish; the owner publishes)
- **Título:** ¿Por qué no todos sentimos igual el sabor de la palta? 🥑
- **Descripción:** La misma palta puede ser cremosa para una persona y casi incomible para otra. No es capricho: el sabor mezcla lengua, olfato y textura, cada persona tiene sensores distintos (por ejemplo, variantes del gen TAS2R38 para ciertos amargos y del receptor OR6A2 para el olor del cilantro) y el cerebro aprende qué le gusta con la infancia, la cultura y la experiencia. Un gusto es biología más aprendizaje, no un error del otro. Envíaselo a ese amigo que odia la palta (o el aguacate).
  Música: "Sneaky Snitch" de Kevin MacLeod (incompetech.com), licencia CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/). *(pista provisional: copiar `audio.music_credit` de scenes.json)*
- **Hashtags:** #shorts #ciencia #sabor #palta #aguacate #curiosidades #comoFunciona

## Script (final, 7 scenes; neutral Latin American Spanish; "palta" as in the owner's hook, "aguacate" in the description)
1. **Hook** — ¿Cómo puede la misma palta ser cremosa para una persona y casi incomible para otra? Cambia la señal que recibe cada cerebro.
2. **Sabor es más que lengua** — Primero, el sabor no es solo la lengua: ella detecta dulce, salado, ácido, amargo y umami, pero gran parte viene del olfato. La textura y la grasa también cuentan.
3. **Sensores distintos** — Segundo, los sensores cambian. Variantes del gen TAS2R38 hacen que ciertos amargos sean intensísimos para unos y casi invisibles para otros. Los supercatadores sienten más, no mejor.
4. **Olfato y cilantro** — Con el olfato pasa igual: por variantes del receptor OR6A2, el cilantro huele a jabón para algunas personas, y fresco para otras.
5. **Por qué divide la palta** — ¿Y la palta? Casi no tiene azúcar ni sal, pero sí mucha grasa: es sobre todo textura. Para uno es mantecosa, para otro pastosa, y según su madurez es casi otra comida.
6. **El cerebro aprende** — Tercero, el cerebro aprende. La infancia, la familia y probar muchas veces moldean el gusto, y una mala experiencia deja huella. La evolución suma: lo graso suena a energía; lo muy amargo, a peligro.
7. **Cierre** — Cada cerebro recibe otra señal del mismo bocado, y la interpreta con su historia. Un gusto es biología más aprendizaje, no un error del otro. Sígueme, y envíaselo a ese amigo que odia la palta.
- **Hook:** the false belief ("the food alone decides the taste") is staged as a contrast: ONE avocado half feeds three identical columns that end at three different heights.
- **Central reframe:** "Un gusto es biología más aprendizaje, no un error del otro."

## Scene plan (one rig, revisited; every sentence changes something)
Hero rig: one stylised avocado half (identical in every scene) above three person-columns. Each column = three sensor towers (TASTE indigo, SMELL lime, TEXTURE butter; tower height and dome size = that person's gain) and a gauge that stacks the three signals. Tokens flow avocado → tower → gauge.
1. Avocado pops on "palta"; tokens flow into three columns on "cremosa" / "incomible" / "Cambia": the three gauges end at three different stacks (P1 bitter-heavy, P2 creamy-heavy, P3 almost no smell).
2. All three persons neutral (gain 1): taste tokens on "lengua", a dense smell stream on "olfato", texture on "textura": the stack builds one segment at a time.
3. The taste towers change per person on "TAS2R38"; a bitter hit (same amount for all) gives three different taste segments; accent ring on the strongest tower on "supercatadores".
4. The avocado leaves; a cilantro sprig pops on "cilantro"; one smell tower gives white foam tokens (soap) on "jabón", the other lime tokens (fresh) on "fresco".
5. Avocado back: taste and smell streams are thin, the texture stream is thick ("mucha grasa"); rings mark two readings; ripeness shifts the avocado colour toward brown while the texture signal dips, recovers, dips ("madurez").
6. Practice lowers one tower's gain stepwise ("veces"); a bad experience raises another tower and drops a wine mark ("mala experiencia"); an energy lamp lights with butter tokens ("energía"), a danger lamp lights with indigo tokens ("peligro").
7. Same avocado, three columns, three signals; the C2 "ENVÍASELO" tag word-locked at "envíaselo".

## Scientific claims, checked (internal fact-check) and simplifications declared
- Taste vs flavour: the tongue's five basic tastes (sweet, salty, sour, bitter, umami) and retronasal smell as a major part of "flavour": supported by standard sensory science. We say "gran parte", never the "80 %" figure (not reliable). Texture, fat and temperature change the experience: supported (oral somatosensation/fat texture).
- TAS2R38: common variants (PAV/AVI) change sensitivity to PTC/PROP-type bitter compounds; well documented. We say "ciertos amargos" and never claim it decides avocado liking. The "supercatadores" (supertasters) perceive more intense taste on average; we say "sienten más, no mejor" (not better taste).
- OR6A2: variants associated with perceiving cilantro as soapy (Eriksson et al., 2012); an association, we say "variantes del receptor". No "avocado gene" is claimed anywhere.
- Avocado: low sugar and salt, subtle aroma, high fat (mostly monounsaturated); the experience is mostly texture/mildness. Ripeness changes texture and aroma: supported.
- Learning: exposure, family, culture change preference; one-trial conditioned taste aversion is real; evolutionary bias (sweet/fat = energy, strong bitter = possible toxins) is background pressure, not destiny.
- Simplifications: three "persons" are columns with gains, not anatomy; amounts are illustrative, no number is shown or claimed. The gains are choreographed, not measured. The guacamole (salt/acid/chilli) beat from the brief was cut for length: stated deviation.

## Colour plan (who decided, why)
- Stage = Coral gradient, background only (identity, unchanged).
- Board (support): pale teal #D2EAE6, **design lens**: derived from the accent system (deep teal lightened), reused from engranajes/reloj/imanes where it measured 31.5-32.3 dE from the stage. Plinth and slots/stems = Coral ink #1D1B2E.
- Hero colours, **design lens** (harmony: three clearly different signal colours that read on the pale board and the ink slots, none near Coral): TASTE indigo #4A2BC4, SMELL lime #C5DB4A, TEXTURE butter #F5D26B; avocado skin deep green #35662E, flesh #C9D96A, pit #7A4A2A; cilantro #3E8E3A; soap foam white. Accent ring = deep teal emissive (identity).
- Marketing lens: the three signal colours double as the legend of the whole video, so the viewer reads "same avocado, three different stacks" with no text.

## Composition gate
Result: PASS on the first run (7 stills, 0 blocks); tables in `build/gate/gate.md`. Lowest pair: support_board vs hero_small 21.2 (above the 20 threshold, narrow); accent vs stage 3.59:1; rendered accent #0A5C6B = swatch (dE 0.0); rendered error #650013 vs swatch #7A0019 (dE 4.1).

## Render and QA
- Rendered through the driver (caffeinate-wrapped) via `tools/chain_render.sh`, gate fresh before every scene. 2,377 frames in 68.3 min = **1.73 s/frame**; final.mp4 **79.23 s**, 1080x1920, 30 fps, 21.4 MB. fal spend US$0.
- `glitch_scan.py 0.8`: no suspect frames in any of the 7 clips.
- Frames inspected at 20 / 40 / 62 / 77 s: avocado, towers, gauges and the three-stack payoff are readable; the word-locked tags (FRESCO etc.) and the closing ENVÍASELO tag appear at the expected words. Positions were estimated from stills: the ENVÍASELO tag (y 0.84) lands on the Coral stage below the plinth, small but legible; the other tags sit over the pale board. I did not watch the video or hear the audio.
- Deviations: 79.2 s is above the 60-75 s target (guacamole beat cut and still long); gate margin support_board vs hero_small is narrow (21.2).
