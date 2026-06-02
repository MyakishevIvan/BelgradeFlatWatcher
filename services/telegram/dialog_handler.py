from telegram import Update
from telegram.ext import (
    ContextTypes,
)

from enums.keyboards_type import KeyboardType
from services.telegram.telegram_search_utils import build_keyboard


class DialogHandler:

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data.clear()
        await update.message.reply_text(
            "This bot can help you to find flats in Belgrade!\nSelect rooms count",
            reply_markup=build_keyboard(keyboard_type=KeyboardType.ROOMS),
        )

    async def handle_rooms(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        context.user_data["rooms_count"] = query.data
        await query.message.reply_text(
            "Select price range",
            reply_markup=build_keyboard(keyboard_type=KeyboardType.PRICE),
        )

    async def handle_price(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        min_price, max_price = map(int, query.data.split(":"))
        context.user_data["min_price"] = min_price
        context.user_data["max_price"] = max_price
        await query.message.reply_text(
            "Select square range",
            reply_markup=build_keyboard(keyboard_type=KeyboardType.SQUARE),
        )

    async def handle_square(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        min_square, max_square = map(int, query.data.split(":"))
        context.user_data["min_square"] = min_square
        context.user_data["max_square"] = max_square
        await query.message.reply_text(
            "Confirm search",
            reply_markup=build_keyboard(KeyboardType.SEARCH)
        )

    async def handle_search(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.message.reply_text(
            f'Searching by filter:\n'
            f'Rooms count:  {context.user_data["rooms_count"]}\n'
            f'Price:  {context.user_data["min_price"]} - {context.user_data["max_price"]}\n'
            f'Square:  {context.user_data["min_square"]} - {context.user_data["max_square"]}\n'
        )
