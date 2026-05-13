import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

from services.search_executor import SearchExecutor
from services.telegram_services.telegram_keyboards import (
    price_keyboard,
    rooms_keyboard,
    square_keyboard,
)
from services.telegram_services.telegram_search_utils import (
    build_filters,
    try_create_flat_messages,
)

ROOMS, PRICE, SQUARE = range(3)


class DialogService:
    def __init__(self, search_executor: SearchExecutor, app: Application) -> None:
        self._search_executor = search_executor
        self._app = app

    def register_handlers(self) -> None:
        conversation = ConversationHandler(
            entry_points=[CommandHandler("start", self._start)],
            states={
                ROOMS: [CallbackQueryHandler(self._handle_rooms)],
                PRICE: [CallbackQueryHandler(self._handle_price)],
                SQUARE: [CallbackQueryHandler(self._handle_square)],
            },
            fallbacks=[CommandHandler("start", self._start)],
            per_message=False,
        )

        self._app.add_handler(conversation)

    async def _start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data.clear()
        await update.message.reply_text(
            "This bot can help you to find flats in Belgrade!\nSelect rooms count",
            reply_markup=rooms_keyboard(),
        )
        return ROOMS

    async def _handle_rooms(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        context.user_data["rooms_count"] = query.data
        await query.message.reply_text(
            "Select price range",
            reply_markup=price_keyboard(),
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
            reply_markup=square_keyboard(),
        )
        return SQUARE

    async def _handle_square(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        min_square, max_square = map(int, query.data.split(":"))
        context.user_data["min_square"] = min_square
        context.user_data["max_square"] = max_square
        return await self._run_search(query, context)

    async def _run_search(self, query, context):
        await query.message.reply_text("Searching...")
        filters = build_filters(context.user_data)
        flats = await asyncio.to_thread(
            self._search_executor.execute,
            filters
        )
        for message in try_create_flat_messages(flats):
            await query.message.reply_text(message, parse_mode="HTML")
        await query.message.reply_text('You can use /subscribe to receive updates once in a day', parse_mode="HTML")
        
        return ConversationHandler.END