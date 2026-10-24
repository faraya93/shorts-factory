"""Smoke test: genera UN clip de video (6 s, 480p, 9:16) con MiniMax Hailuo en fal.ai."""

import os
import struct
import sys
import time
import urllib.request
from pathlib import Path

import fal_client
from dotenv import load_dotenv

ENDPOINT = "minimax/h3-max-turbo/text-to-video"
PROMPT = (
    "Stylized 3D medical animation, close-up of a deep clean cut on a forearm, "
    "wound edges apart, dramatic lighting, vertical 9:16, educational, no gore"
)
ARGUMENTS = {
    "prompt": PROMPT,
    "duration": 6,
    "resolution": "480P",
    "aspect_ratio": "9:16",
    "prompt_expansion_mode": "balanced",
}

# USD por segundo de video a 480p (fal.ai). La promo del 35% termina el 31 de octubre.
PRICE_PROMO = 0.01625
PRICE_STANDARD = 0.025

POLL_SECONDS = 3
OUTPUT = Path("output/smoke.mp4")


def mp4_duration(path: Path) -> float | None:
    """Lee la duración real del átomo mvhd del MP4 (sin depender de ffprobe)."""
    data = path.read_bytes()
    i = data.find(b"mvhd")
    if i < 0:
        return None
    version = data[i + 4]
    if version == 1:
        timescale, duration = struct.unpack(">IQ", data[i + 24 : i + 36])
    else:
        timescale, duration = struct.unpack(">II", data[i + 16 : i + 24])
    return duration / timescale if timescale else None


def main() -> int:
    load_dotenv()
    if not os.getenv("FAL_KEY"):
        print("Falta FAL_KEY. Copia .env.example a .env y pega tu llave.")
        return 1

    print(f"Enviando trabajo a {ENDPOINT} ...")
    handle = fal_client.submit(ENDPOINT, arguments=ARGUMENTS)
    print(f"request_id: {handle.request_id}")

    start = time.monotonic()
    last = None
    while True:
        status = handle.status(with_logs=True)
        elapsed = int(time.monotonic() - start)
        if isinstance(status, fal_client.Queued):
            line = f"EN COLA (posición {status.position})"
        elif isinstance(status, fal_client.InProgress):
            line = "GENERANDO"
            for log in status.logs or []:
                print(f"   log: {log.get('message')}")
        else:
            print(f"[{elapsed:>3}s] COMPLETADO")
            break
        if line != last:
            print(f"[{elapsed:>3}s] {line}")
            last = line
        time.sleep(POLL_SECONDS)

    result = handle.get()
    video_url = result["video"]["url"]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(video_url, OUTPUT)

    real = mp4_duration(OUTPUT)
    billed = real if real else ARGUMENTS["duration"]

    print("\n--- Resultado ---")
    print(f"URL:        {video_url}")
    print(f"Archivo:    {OUTPUT} ({OUTPUT.stat().st_size / 1024:.0f} KB)")
    print(f"Duración:   {f'{real:.2f} s' if real else 'no disponible'}")
    print(f"Inferencia: {result.get('timings', {}).get('inference', 'n/d')} s")
    print("Costo:      la API no lo reporta; estimación por duración real:")
    print(f"            ${billed * PRICE_PROMO:.4f} (promo hasta 31-oct) / "
          f"${billed * PRICE_STANDARD:.4f} (tarifa normal)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
