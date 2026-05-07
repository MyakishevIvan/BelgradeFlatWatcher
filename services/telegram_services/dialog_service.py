import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from pages.components.flat_components.flat import Flat
from services.search_filters import SearchFilters
from services.search_service import SearchService
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler, Application,
)

ROOMS, PRICE, SQUARE = range(3)
CHAR_LIMIT = 4096


class DialogService:
    def __init__(self, search_service: SearchService, app: Application):
        self._search_service = search_service
        self._app = app

    def register_handlers(self) -> None:
        conversation = ConversationHandler(
            entry_points=[CommandHandler("search", self._search)],
            states={
                ROOMS: [CallbackQueryHandler(self._handle_rooms)],
                PRICE: [CallbackQueryHandler(self._handle_price)],
                SQUARE: [CallbackQueryHandler(self._handle_square)],
            },
            fallbacks=[CommandHandler("reset", self._reset)],
        )

        self._app.add_handler(CommandHandler("start", self._start))
        self._app.add_handler(CommandHandler("reset", self._reset))
        self._app.add_handler(conversation)

    async def _search(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data.clear()

        await update.message.reply_text(
            "Select rooms count",
            reply_markup=self._rooms_keyboard(),
        )
        return ROOMS

    async def _handle_rooms(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()

        context.user_data["rooms_count"] = int(query.data)

        await query.message.reply_text(
            "Select price range",
            reply_markup=self._price_keyboard(),
        )
        return PRICE

    async def _handle_price(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()

        min_price, max_price = map(int, query.data.split(":"))
        context.user_data["min_price"] = min_price
        context.user_data["max_price"] = max_price

        await query.message.reply_text(
            "Select square range",
            reply_markup=self._square_keyboard(),
        )
        return SQUARE

    async def _handle_square(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()

        min_square, max_square = map(int, query.data.split(":"))
        context.user_data["min_square"] = min_square
        context.user_data["max_square"] = max_square

        filters = self._build_filters(context)

        await query.message.reply_text(f"{filters}\nWaiting...")

        flats = await asyncio.to_thread(
            self._search_service.get_all_flats,
            filters,
        )

        if not flats:
            await query.message.reply_text("No flats found")
            return ConversationHandler.END

        await self._send_flats(query.message, flats)
        return ConversationHandler.END

    def _build_filters(self, context: ContextTypes.DEFAULT_TYPE) -> SearchFilters:
        return SearchFilters(
            min_price=context.user_data["min_price"],
            max_price=context.user_data["max_price"],
            min_square=context.user_data["min_square"],
            max_square=context.user_data["max_square"],
            rooms_count=context.user_data["rooms_count"],
        )

    async def _send_flats(self, message, flats: list[Flat]) -> None:
        for text in self._create_messages(flats):
            await message.reply_text(text, parse_mode="HTML")

    def _rooms_keyboard(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("one bedroom", callback_data="1")],
            [InlineKeyboardButton("two bedroom", callback_data="2")],
            [InlineKeyboardButton("three bedroom", callback_data="3")],
        ])

    def _price_keyboard(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("100-250", callback_data="100:250")],
            [InlineKeyboardButton("250-1000", callback_data="250:1000")],
            [InlineKeyboardButton("1000-3000", callback_data="1000:3000")],
        ])

    def _square_keyboard(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("10-35", callback_data="10:35")],
            [InlineKeyboardButton("35-65", callback_data="35:65")],
            [InlineKeyboardButton("65-150", callback_data="65:150")],
        ])