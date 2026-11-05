"""Contact sheet of PNG stills side by side (for visual review). .venv/bin/python tools/contact_sheet.py out.png in1.png in2.png ..."""
import sys
from PIL import Image
ims = [Image.open(p).convert("RGB") for p in sys.argv[2:]]
w, h = ims[0].size
s = Image.new("RGB", (w * len(ims), h))
for i, im in enumerate(ims):
    s.paste(im.resize((w, h)), (i * w, 0))
s.thumbnail((2400, 1400))
s.save(sys.argv[1])
