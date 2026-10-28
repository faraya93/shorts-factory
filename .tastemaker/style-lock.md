# Style lock — shorts-factory drawn channel (PROPOSED 2026-10-27, pending owner approval; see docs/design-system.md)
Direction contract: thesis = "look inside everyday objects on a bright, constant celeste stage"; first frame = real-colour hero on a navy plinth, caption band clear; risk = accent legibility on a light stage.
## Colour contract (verified with tools/palette_metrics.py, WCAG 2.x)
| pair | ratio | verdict |
|---|---|---|
| navy #0B2540 on stage top #8FD6F2 / bottom #62B4DC | 9.66 / 6.71 | text-safe (>=4.5) |
| white on navy box | 15.52 | text-safe |
| ember #E8590C on stage top / bottom | 2.23 / 1.55 | graphics only, never text; relies on hue (dE2000 55 / 53) |
| error #C92A2A on stage top / bottom | 3.4 / 2.36 | UI-safe only on the top end; add outline |
| plinth #2B4C70 on stage bottom | 3.83 | UI-safe |
Illegal: white or grey text directly on the stage (1.4-1.8); gold #F5C04A on the stage (1.1).
## Type: Montserrat ExtraBold (+ SemiBold for non-spoken words). Mode: light stage, dark-ink text theme.
