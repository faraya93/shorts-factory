"""Overlay helper for script.json authoring (python import): tag(text, word, x, y, vis=1.6, off=0.0), mark, counter, bar."""
def tag(text, word, x, y, vis=1.6, off=0.0):
    return {"type": "label", "style": "tag", "text_or_value": text, "at_word": word, "offset_s": off, "visible_s": vis, "x": x, "y": y}
def counter(text, word, x, y, dur=1.2, vis=2.5, off=0.0, frm=None):
    d = {"type": "counter", "style": "mono", "text_or_value": text, "at_word": word, "offset_s": off, "visible_s": vis, "x": x, "y": y}
    if frm is not None: d["from"] = frm
    return d
def mark(kind, word, x, y, off=0.0):
    return {"type": "mark", "kind": kind, "x": x, "y": y, "at_word": word, "offset_s": off}
def send(word="envíaselo"):
    return {"type": "label", "style": "tag", "text_or_value": "ENVÍASELO", "at_word": word, "duration_s": 2.6, "x": 0.5, "y": 0.84}
def apply(path, per_scene):
    import json
    d = json.load(open(path)); 
    for i, ovs in per_scene.items(): d["scenes"][i - 1]["overlays"] = ovs
    json.dump(d, open(path, "w"), ensure_ascii=False, indent=1)
