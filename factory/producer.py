"""Producer (Fase A): genera los clips de una producción a partir de su scenes.json.

Uso: python factory/producer.py productions/<canal>/<video> [--yes]
"""

import argparse
import hashlib
import json
import math
import subprocess
import sys
import time
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

import fal_client
from dotenv import load_dotenv

SCHEMA_URL = "https://fal.ai/api/openapi/queue/openapi.json?endpoint_id={}"

# USD por segundo de video a 480p (fal.ai). La API no reporta costo, así que se estima.
# El gate y el tope usan la tarifa normal (conservadora); la promo vence el 2026-10-31.
RATE_STANDARD = 0.025
RATE_PROMO = 0.01625
PROMO_UNTIL = date(2026, 10, 31)

CONFIRM_OVER_USD = 1.0
HARD_CAP_USD = 3.0
MAX_ATTEMPTS = 2
POLL_SECONDS = 3


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fetch_input_schema(model: str) -> dict:
    with urllib.request.urlopen(SCHEMA_URL.format(model), timeout=30) as r:
        schemas = json.load(r)["components"]["schemas"]
    name = next(n for n in schemas if n.endswith("Input"))
    return schemas[name]["properties"]


def snap_duration(target: float, prop: dict) -> tuple[float, str | None]:
    """Devuelve (duración válida >= target, nota del ajuste o None)."""
    allowed = prop.get("enum")
    if allowed:
        ok = [v for v in sorted(allowed) if v >= target]
        value = ok[0] if ok else max(allowed)
    else:
        value = min(max(target, prop.get("minimum", 0)), prop.get("maximum", math.inf))
        step = prop.get("multipleOf")
        if step:
            value = math.ceil(value / step) * step
    note = None if value == target else f"{target} s -> {value} s"
    if value < target:
        note = f"{target} s -> {value} s (el modelo no permite más; queda MÁS CORTA)"
    return value, note


def probe(path: Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height:format=duration",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    info = json.loads(out.stdout)
    stream = info["streams"][0]
    return {"width": stream["width"], "height": stream["height"],
            "duration": float(info["format"]["duration"])}


def validate_clip(path: Path) -> dict | None:
    """Metadatos si el clip es válido (vertical 9:16, 480 en una dimensión), si no None."""
    try:
        meta = probe(path)
    except (subprocess.CalledProcessError, KeyError, IndexError, ValueError):
        return None
    w, h = meta["width"], meta["height"]
    if meta["duration"] <= 0 or h <= w or abs(w / h - 9 / 16) > 0.03 or 480 not in (w, h):
        return None
    return meta


def wait_for(model: str, request_id: str) -> dict:
    start = time.monotonic()
    last = None
    while True:
        status = fal_client.status(model, request_id, with_logs=True)
        if isinstance(status, fal_client.Queued):
            line = f"EN COLA (posición {status.position})"
        elif isinstance(status, fal_client.InProgress):
            line = "GENERANDO"
        else:
            print(f"   [{int(time.monotonic() - start):>3}s] COMPLETADO")
            return fal_client.result(model, request_id)
        if line != last:
            print(f"   [{int(time.monotonic() - start):>3}s] {line}")
            last = line
        time.sleep(POLL_SECONDS)


class Costs:
    """costs.json: semilla de la producción + una entrada por intento de generación."""

    def __init__(self, path: Path, model: str, default_seed: int):
        self.path = path
        if path.exists():
            self.data = json.loads(path.read_text())
        else:
            self.data = {"model": model, "seed": default_seed, "entries": []}

    @property
    def seed(self) -> int:
        return self.data["seed"]

    def save(self) -> None:
        self.path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False) + "\n")

    def add(self, entry: dict) -> dict:
        self.data["entries"].append(entry)
        self.save()
        return entry

    def pending(self, scene_id: int) -> dict | None:
        """Último trabajo enviado de la escena que nunca se cerró (proceso interrumpido)."""
        for e in reversed(self.data["entries"]):
            if e["scene"] == scene_id:
                return e if e["status"] == "submitted" else None
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("production", type=Path)
    ap.add_argument("--yes", action="store_true", help="confirma de antemano si el total supera US$1")
    ap.add_argument("--max-spend", type=float, default=HARD_CAP_USD,
                    help="hard cap in US$ for this run (default %.2f)" % HARD_CAP_USD)
    args = ap.parse_args()

    load_dotenv()
    prod = args.production
    cfg = json.loads((prod / "scenes.json").read_text())
    model, resolution = cfg["model"], cfg["resolution"]
    clips = prod / "clips"
    clips.mkdir(exist_ok=True)

    schema = fetch_input_schema(model)
    if resolution not in schema["resolution"].get("enum", [resolution]):
        print(f"El modelo no acepta resolution={resolution}")
        return 1
    rate = RATE_STANDARD
    promo = RATE_PROMO if date.today() <= PROMO_UNTIL else RATE_STANDARD

    default_seed = int(hashlib.sha256(f"{cfg['channel']}/{cfg['video']}".encode()).hexdigest(), 16) % 2**31
    costs = Costs(prod / "costs.json", model, default_seed)
    use_seed = "seed" in schema
    expansion = "disabled" if "prompt_expansion_mode" in schema else None

    # --- Plan: duración ajustada y estimado por escena ---
    plan = []
    print(f"Producción: {cfg['title']}  |  modelo {model}  |  {resolution}  |  seed {costs.seed if use_seed else 'n/a'}")
    print(f"prompt_expansion_mode: {expansion or 'NO soportado por el esquema'}\n")
    print(f"{'esc':<4}{'nombre':<15}{'target':>7}{'pedida':>8}{'est. (tarifa normal)':>22}{'est. (promo)':>14}  estado")
    for s in cfg["scenes"]:
        dur, note = snap_duration(s["target_duration_s"], schema["duration"])
        done = validate_clip(clips / f"scene-{s['id']:02d}.mp4")
        plan.append({"scene": s, "duration": dur, "done": done is not None})
        cost = 0 if done else dur * rate
        promo_cost = 0 if done else dur * promo
        print(f"{s['id']:<4}{s['name']:<15}{s['target_duration_s']:>6}s{dur:>7}s"
              f"{'$%.4f' % cost:>22}{'$%.4f' % promo_cost:>14}  {'ya existe, se omite' if done else 'pendiente'}")
    adjustments = [f"escena {p['scene']['id']}: {n}" for p in plan
                   if (n := snap_duration(p["scene"]["target_duration_s"], schema["duration"])[1])]
    print("\nAjustes de duración:", "; ".join(adjustments) if adjustments else "ninguno (todos dentro del rango permitido)")
    print(f"Rango permitido: {schema['duration'].get('minimum')}–{schema['duration'].get('maximum')} s; "
          "el modelo puede entregar hasta ~0.7 s más de lo pedido.")

    pending = [p for p in plan if not p["done"]]
    total = sum(p["duration"] * rate for p in pending)
    print(f"\nTOTAL ESTIMADO: ${total:.4f} (tarifa normal ${rate}/s)  |  con promo: "
          f"${sum(p['duration'] * promo for p in pending):.4f}  |  tope duro ${args.max_spend:.2f}")
    if not pending:
        print("Nada que generar.")
        return 0
    if total > CONFIRM_OVER_USD and not args.yes:
        try:
            answer = input(f"El total supera US${CONFIRM_OVER_USD:.2f}. ¿Continuar? [s/N] ")
        except EOFError:
            answer = ""
        if answer.strip().lower() not in ("s", "si", "sí", "y", "yes"):
            print("\nCancelado, no se gastó nada.")
            return 0

    # --- Generación ---
    spent, done_ids, failed_ids = 0.0, [], []
    for p in pending:
        s, dur = p["scene"], p["duration"]
        target_file = clips / f"scene-{s['id']:02d}.mp4"
        prompt = f"{cfg['style']} {s['prompt']}"
        if cfg.get("audio_style"):  # optional; appended to every generation prompt
            prompt += f" {cfg['audio_style']}"
        arguments = {"prompt": prompt, "duration": dur, "resolution": resolution,
                     "aspect_ratio": cfg["aspect_ratio"]}
        if expansion:
            arguments["prompt_expansion_mode"] = expansion
        if use_seed:
            arguments["seed"] = costs.seed

        print(f"\n== Escena {s['id']} ({s['name']}) ==")
        stale = costs.pending(s["id"])  # trabajo ya pagado cuya descarga se interrumpió
        ok = False
        for attempt in range(1, MAX_ATTEMPTS + 1):
            if spent + dur * rate > args.max_spend:
                print(f"TOPE DE ${args.max_spend:.2f} alcanzado (gastado ${spent:.4f}); me detengo.")
                _summary(done_ids, failed_ids, spent)
                return 2
            entry = None
            try:
                if stale and attempt == 1:
                    print(f"   recuperando trabajo previo {stale['request_id']} (sin pagar de nuevo)")
                    entry, rid = stale, stale["request_id"]
                else:
                    print(f"   intento {attempt}/{MAX_ATTEMPTS}: enviando trabajo")
                    rid = fal_client.submit(model, arguments=arguments).request_id
                    entry = costs.add({"scene": s["id"], "name": s["name"], "model": model,
                                       "request_id": rid, "status": "submitted", "attempt": attempt,
                                       "requested_duration_s": dur, "seed": costs.seed if use_seed else None,
                                       "submitted_at": now()})
                result = wait_for(model, rid)
                tmp = target_file.with_suffix(".part")
                urllib.request.urlretrieve(result["video"]["url"], tmp)
                meta = validate_clip(tmp)
                real = meta["duration"] if meta else dur
                cost = real * rate  # el trabajo se cobra aunque el clip no valide
                if not (stale and attempt == 1):
                    spent += cost
                if meta is None:
                    tmp.unlink(missing_ok=True)
                    entry.update(status="invalid_clip", estimated_cost_usd=round(cost, 5), finished_at=now())
                    costs.save()
                    print("   clip inválido en ffprobe (no es 9:16 / 480p)")
                    continue
                tmp.rename(target_file)
                entry.update(status="ok", real_duration_s=round(real, 3),
                             resolution=f"{meta['width']}x{meta['height']}",
                             video_url=result["video"]["url"], estimated_cost_usd=round(cost, 5),
                             finished_at=now())
                costs.save()
                print(f"   OK: {meta['width']}x{meta['height']}, {real:.2f} s, ~${cost:.4f}")
                ok = True
                break
            except Exception as e:  # noqa: BLE001 - cualquier fallo de red/API cuenta como intento
                print(f"   error: {e}")
                if entry is not None:
                    entry.update(status="error", error=str(e), finished_at=now())
                    costs.save()
        (done_ids if ok else failed_ids).append(s["id"])
        if not ok:
            print(f"   escena {s['id']} marcada como FALLIDA tras {MAX_ATTEMPTS} intentos; sigo con la siguiente")

    _summary(done_ids, failed_ids, spent)
    return 1 if failed_ids else 0


def _summary(done: list, failed: list, spent: float) -> None:
    print("\n=== Resumen ===")
    print(f"Escenas generadas: {len(done)} {done}")
    print(f"Escenas fallidas:  {len(failed)} {failed}")
    print(f"Costo estimado de esta corrida: ${spent:.4f} (tarifa normal)")


if __name__ == "__main__":
    sys.exit(main())
