from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

from services.search_executor import SearchExecutor
from telegram_services.telegram_keyboards import price_keyboard, rooms_keyboard, square_keyboard
from telegram_services.telegram_search_utils import build_filters, create_flat_messages, execute_search

ROOMS, PRICE, SQUARE = range(3)


class DialogService:
    def __init__(self, search_executor: SearchExecutor, app: Application) -> None:
        self._search_executor = search_executor
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
            per_message=False,
        )

        self._app.add_handler(CommandHandler("start", self._start))
        self._app.add_handler(CommandHandler("reset", self._reset))
        self._app.add_handler(conversation)

    async def _start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Hi, use /search to find flats")

    async def _reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data.clear()
        await update.message.reply_text("Filter was cleaned. You can start again with /search")
        return ConversationHandler.END

    async def _search(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data.clear()
        await update.message.reply_text("Select rooms count", reply_markup=rooms_keyboard())
        return ROOMS

    async def _handle_rooms(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()

        context.user_data["rooms_count"] = query.data

        await query.message.reply_text("Select price range", reply_markup=price_keyboard())
        return PRICE

    async def _handle_price(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()

        min_price, max_price = map(int, query.data.split(":"))
        context.user_data["min_price"] = min_price
        context.user_data["max_price"] = max_price

        await query.message.reply_text("Select square range", reply_markup=square_keyboard())
        return SQUARE

    async def _handle_square(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()

        min_square, max_square = map(int, query.data.split(":"))
        context.user_data["min_square"] = min_square
        context.user_data["max_square"] = max_square

        filters = build_filters(context.user_data)
        await query.message.reply_text(f"{filters}\nWaiting...")

        flats = await execute_search(self._search_executor, filters)

        if not flats:
            await query.message.reply_text("No flats found")
            return ConversationHandler.END

        messages = create_flat_messages(flats)
        for message in messages:
            await query.message.reply_text(message, parse_mode="HTML")

        return ConversationHandler.END