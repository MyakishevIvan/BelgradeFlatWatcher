import asyncio
from typing import Any

from data_base.models.seen_flats_model import SeenFlat
from data_base.models.subscriptions_model import Subscription
from pages.components.flat_components.flat import Flat
from services.search_executor import SearchExecutor
from services.search_filters import SearchFilters

CHAR_LIMIT = 4096

FILTER_FIELDS = (
    "min_square",
    "max_square",
    "min_price",
    "max_price",
    "rooms_count",
)


def build_filters(data: dict[str, Any]) -> SearchFilters:
    return SearchFilters(
        min_price=data["min_price"],
        max_price=data["max_price"],
        min_square=data["min_square"],
        max_square=data["max_square"],
        rooms_type=data["rooms_count"],
    )


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


def get_missing_filter_fields(data: dict[str, Any]) -> list[str]:
    return [
        field
        for field in FILTER_FIELDS
        if field not in data or data[field] is None
    ]


def extract_filters_data(data: dict[str, Any]) -> dict[str, Any]:
    return {field: data[field] for field in FILTER_FIELDS}


def try_create_flat_messages(flats: list[Flat], error_message: str = 'Flats not found') -> list[str]:
    if not flats:
        return [error_message]

    messages: list[str] = []
    message = ""

    for flat in flats:
        flat_str = f"{flat}\n"

        if len(message) + len(flat_str) > CHAR_LIMIT:
            if message:
                messages.append(message)
            message = flat_str
        else:
            message += flat_str

    if message:
        messages.append(message)

    return messages
