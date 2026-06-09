import json
from pathlib import Path
from typing import Any


_BASE_DIR = Path(__file__).parents[1]
_CONFIG_DIR = _BASE_DIR / "configs"


def _load_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


class Config:
    SEARCH = _load_config(_CONFIG_DIR / "search_config.json")
    SELENIUM = _load_config(_CONFIG_DIR / "selenium_config.json")
    KEYBOARDS = SEARCH["KEYBOARD"]
    SUBSCRIPTIONS = _load_config(_CONFIG_DIR / "subscription_config.json")
