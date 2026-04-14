import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from pages.components.flat_components.flat import Flat
from services.search_filters import SearchFilters
from services.search_service import SearchService
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

ROOMS, PRICE, SQUARE = range(3)
CHAR_LIMIT = 4096


class TelegramService:
    def __init__(self, token: str, search_service: SearchService):
        self._search_service = search_service
        self._app = ApplicationBuilder().token(token).build()
        self._register_handlers()

    def _register_handlers(self) -> None:
        search_conversation = ConversationHandler(
            entry_points=[CommandHandler("search", self._search)],
            states={
                ROOMS: [CallbackQueryHandler(self._handle_rooms)],
                PRICE: [CallbackQueryHandler(self._handle_price)],
                SQUARE: [CallbackQueryHandler(self._handle_square)],
            },
            fallbacks=[CommandHandler("search", self._search)],
        )

        self._app.add_handler(CommandHandler("start", self._start))
        self._app.add_handler(CommandHandler("reset", self._reset))
        self._app.add_handler(search_conversation)

    async def _start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text('Hi, use /search for find flats')

    async def _reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        context.user_data.clear()
        await update.message.reply_text("Filter was cleaned.You can start again/search")
        return ConversationHandler.END
    
    async def _search(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data.clear()
        keyboard = [
            [InlineKeyboardButton(text='one bedroom', callback_data='1')],
            [InlineKeyboardButton(text='two bedroom', callback_data='2')],
            [InlineKeyboardButton(text='three bedroom', callback_data='3')],
        ]
        await update.message.reply_text("Select rooms count",
                                        reply_markup=InlineKeyboardMarkup(keyboard))
        return ROOMS

    async def _handle_rooms(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        rooms_count = query.data
        context.user_data['rooms_count'] = rooms_count
        keyboard = [
            [InlineKeyboardButton(text='100-250', callback_data='100:250')],
            [InlineKeyboardButton(text='250-1000', callback_data='250:1000')],
            [InlineKeyboardButton(text='1000-3000', callback_data='1000:3000')],
        ]
        await query.message.reply_text("Select price range",
                                        reply_markup=InlineKeyboardMarkup(keyboard))
        return PRICE

    async def _handle_price(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        min_price, max_price = query.data.split(':')
        context.user_data['min_price'] = min_price
        context.user_data['max_price'] = max_price
        keyboard = [
            [InlineKeyboardButton(text='10-35', callback_data='10:35')],
            [InlineKeyboardButton(text='35-65', callback_data='35:65')],
            [InlineKeyboardButton(text='65-150', callback_data='65:150')],
        ]
        await query.message.reply_text("Select square range",
                                        reply_markup=InlineKeyboardMarkup(keyboard))
        return SQUARE

    async def _handle_square(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        min_square, max_square = query.data.split(':')
        min_price = context.user_data['min_price']
        max_price = context.user_data['max_price']
        rooms_count = context.user_data['rooms_count']
        filters = SearchFilters(
            min_price=min_price,
            max_price=max_price,
            min_square=min_square,
            max_square=max_square,
            rooms_count=rooms_count
        )
        await query.message.reply_text(f'{str(filters)} \n Waiting...')
        flats = await asyncio.to_thread(self._search_service.get_all_flats, filters)
        if not flats:
            await query.message.reply_text('No flats found')
            return ConversationHandler.END

        messages = self._create_messages(flats)
        for message in messages:
            await query.message.reply_text(message, parse_mode="HTML")
        return ConversationHandler.END

    def _create_messages(self, flats: list[Flat]) -> list[str]:
        messages = []
        message = ''
        
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
            
            
    def run(self):
        self._app.run_polling()
