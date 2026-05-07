import asyncio

from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, ConversationHandler

from pages.components.flat_components.flat import Flat
from services.search_filters import SearchFilters
from services.search_service import SearchService

CHAR_LIMIT = 4096
class SubscribeService:
    def __init__(self, app: Application, search_service: SearchService):
        self._app = app
        self._search_service = search_service

    def register_handlers(self):
        self._app.add_handler(CommandHandler("subscribe", self._subscribe))
        self._app.add_handler(CommandHandler("unsubscribe", self._unsubscribe))
    
    async def _subscribe(self, update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
    
        required_fields = [
            "min_square",
            "max_square",
            "min_price",
            "max_price",
            "rooms_count",
        ]
    
        missing_fields = [
            field for field in required_fields
            if field not in context.user_data or context.user_data[field] is None
        ]
    
        if missing_fields:
            await update.message.reply_text(
                "Сначала заполни фильтр через /search.\n"
                f"Не хватает данных: {', '.join(missing_fields)}"
            )
            return
    
        filters_data = {
            "min_square": context.user_data["min_square"],
            "max_square": context.user_data["max_square"],
            "min_price": context.user_data["min_price"],
            "max_price": context.user_data["max_price"],
            "rooms_count": context.user_data["rooms_count"],
        }
    
        # удаляем старую подписку, если была
        for job in context.job_queue.get_jobs_by_name(str(chat_id)):
            job.schedule_removal()
    
        context.job_queue.run_repeating(
            callback=self._send_new_flats,
            interval=60 * 10,  # каждые 10 минут
            first=10,
            chat_id=chat_id,
            name=str(chat_id),
            data=filters_data,
        )
    
        await update.message.reply_text("Подписка включена.")

    async def _unsubscribe(self, update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
    
        jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    
        if not jobs:
            await update.message.reply_text("Активной подписки нет.")
            return
    
        for job in jobs:
            job.schedule_removal()
    
        await update.message.reply_text("Подписка отключена.")


    async def _send_new_flats(self, context: ContextTypes.DEFAULT_TYPE):
        chat_id = context.job.chat_id
        data = context.job.data
    
        filters = SearchFilters(
            min_price=data["min_price"],
            max_price=data["max_price"],
            min_square=data["min_square"],
            max_square=data["max_square"],
            rooms_count=data["rooms_count"],
        )
    
        flats = await asyncio.to_thread(
            self._search_service.get_all_flats,
            filters,
        )
    
        if not flats:
            return
    
        messages = self._create_messages(flats)
    
        for message in messages:
            await context.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode="HTML",
            )

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
        