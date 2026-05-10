from telegram import InlineKeyboardButton, InlineKeyboardMarkup


ROOMS_OPTIONS = [
    ("one bedroom", "1"),
    ("two bedroom", "2"),
    ("three bedroom", "3"),
]

PRICE_OPTIONS = [
    ("100-250", "100:250"),
    ("250-1000", "250:1000"),
    ("1000-3000", "1000:3000"),
]

SQUARE_OPTIONS = [
    ("10-35", "10:35"),
    ("35-65", "35:65"),
    ("65-150", "65:150"),
]


def build_keyboard(options: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text, callback_data=data)]
        for text, data in options
    ])


def rooms_keyboard() -> InlineKeyboardMarkup:
    return build_keyboard(ROOMS_OPTIONS)


def price_keyboard() -> InlineKeyboardMarkup:
    return build_keyboard(PRICE_OPTIONS)


def square_keyboard() -> InlineKeyboardMarkup:
    return build_keyboard(SQUARE_OPTIONS)