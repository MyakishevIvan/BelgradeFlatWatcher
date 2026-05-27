import json
from pathlib import Path
from typing import Any

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from data_base.models.seen_flats_model import SeenFlat
from data_base.models.subscriptions_model import Subscription
from enums.key_boards import KeyboardType
from pages.components.flat_components.flat import Flat
from services.search_filters import SearchFilters


_CONFIG_PATH = Path(__file__).parents[2] / "config/search_config.json"

def _load_search_config() -> dict[str, Any]:
    with _CONFIG_PATH.open(encoding="utf-8") as file:
        return json.load(file)

_CONFIG = _load_search_config()
_KEYBOARDS = _CONFIG["KEYBOARD"]


def build_filters(data: dict[str, Any]) -> SearchFilters:
    if missing_fields := _check_missing_fields(data):
        raise ValueError(f"Missing fields: {', '.join(missing_fields)}")
    
    return SearchFilters(
        min_price=data["min_price"],
        max_price=data["max_price"],
        min_square=data["min_square"],
        max_square=data["max_square"],
        rooms_type=data["rooms_count"],
    )

def _check_missing_fields(data: dict[str, Any]) -> list[str]:
    return [
        field
        for field in _CONFIG["FIELDS"]
        if field not in data or data[field] is None
    ]

def build_filters_from_model(subscription: Subscription) -> SearchFilters:
    return SearchFilters(
        min_price=str(subscription.min_price),
        max_price=str(subscription.max_price),
        min_square=str(subscription.min_square),
        max_square=str(subscription.max_square),
        rooms_type=subscription.rooms_type
    )

def convert_to_model(flats: list[Flat], user_id) -> list[SeenFlat]:
    return [SeenFlat.from_flat(user_id, flat) for flat in flats]

def extract_filters_data(data: dict[str, Any]) -> dict[str, Any]:
    return {field: data[field] for field in _CONFIG["FIELDS"]}

def build_keyboard(keyboard_type: KeyboardType) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text, callback_data=data)]
        for text, data in _KEYBOARDS[keyboard_type]
    ])

def try_create_flat_messages(flats: list[Flat], error_message: str = 'Flats not found') -> list[str]:
    if not flats:
        return [error_message]

    messages: list[str] = []
    message = ""

    for flat in flats:
        flat_str = f"{flat}\n"

        if len(message) + len(flat_str) > _CONFIG['CHAR_LIMIT']:
            if message:
                messages.append(message)
            message = flat_str
        else:
            message += flat_str

    if message:
        messages.append(message)

    return messages
