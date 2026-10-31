"""Channel packages: a BRAND package (channels/<brand>/brand.yaml, language-independent) and thin CHANNEL variants that EXTEND it
(channels/<brand>/<lang>.yaml, only what differs). `load("mecanalia-es")` returns the merged config: a channel value wins, a missing value
inherits the brand's; dicts merge key by key, lists and scalars are replaced whole. Consumers read the config through this module (identity.py,
the Editor, tools); the orchestrator requests a production by channel id and never copies values. No platform credentials ever live here."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CHANNELS = ROOT / "channels"
DEFAULT_CHANNEL = "mecanalia-es"
BRAND_FILE = "brand.yaml"


def _yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def deep_merge(base: dict, over: dict) -> dict:
    out = dict(base)
    for k, v in over.items():
        out[k] = deep_merge(base[k], v) if isinstance(v, dict) and isinstance(base.get(k), dict) else v
    return out


def variants() -> dict[str, Path]:
    """channel id -> variant file, for every channel package on disk."""
    found = {}
    for f in sorted(CHANNELS.glob("*/*.yaml")):
        if f.name != BRAND_FILE:
            found[_yaml(f).get("channel", f.stem)] = f
    return found


def path_of(channel_id: str) -> Path:
    try:
        return variants()[channel_id]
    except KeyError:
        raise KeyError(f"unknown channel '{channel_id}' (known: {', '.join(variants())})") from None


def load_brand(brand: str) -> dict:
    return _yaml(CHANNELS / brand / BRAND_FILE)


def load(channel_id: str = DEFAULT_CHANNEL) -> dict:
    """Merged config of one channel (brand + variant)."""
    var = _yaml(path_of(channel_id))
    return deep_merge(load_brand(var["extends"]), var)
