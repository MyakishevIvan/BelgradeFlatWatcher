import asyncio
from typing import Any

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
        rooms_count=data["rooms_count"],
    )


def get_missing_filter_fields(data: dict[str, Any]) -> list[str]:
    return [
        field
        for field in FILTER_FIELDS
        if field not in data or data[field] is None
    ]


def extract_filters_data(data: dict[str, Any]) -> dict[str, Any]:
    return {field: data[field] for field in FILTER_FIELDS}


async def execute_search(search_executor: SearchExecutor, filters: SearchFilters) -> list[Flat]:
    return await asyncio.to_thread(search_executor.execute, filters)


def create_flat_messages(flats: list[Flat]) -> list[str]:
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