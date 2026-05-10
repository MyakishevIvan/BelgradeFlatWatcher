from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from services.search_executor import SearchExecutor
from telegram_services.telegram_search_utils import (
    build_filters,
    create_flat_messages,
    execute_search,
    extract_filters_data,
    get_missing_filter_fields,
)


class SubscribeService:
    def __init__(self, search_executor: SearchExecutor, app: Application) -> None:
        self._search_executor = search_executor
        self._app = app

    def register_handlers(self) -> None:
        self._app.add_handler(CommandHandler("subscribe", self._subscribe))
        self._app.add_handler(CommandHandler("unsubscribe", self._unsubscribe))

    async def _subscribe(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.effective_chat.id
        missing_fields = get_missing_filter_fields(context.user_data)

        if missing_fields:
            await update.message.reply_text(
                "Сначала заполни фильтр через /search.\n"
                f"Не хватает данных: {', '.join(missing_fields)}"
            )
            return

        self._remove_existing_jobs(context, chat_id)

        context.job_queue.run_repeating(
            callback=self._send_new_flats,
            interval=60 * 10,
            first=10,
            chat_id=chat_id,
            name=str(chat_id),
            data=extract_filters_data(context.user_data),
        )

        await update.message.reply_text("Подписка включена.")

    async def _unsubscribe(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.effective_chat.id
        jobs = context.job_queue.get_jobs_by_name(str(chat_id))

        if not jobs:
            await update.message.reply_text("Активной подписки нет.")
            return

        self._remove_existing_jobs(context, chat_id)
        await update.message.reply_text("Подписка отключена.")

    async def _send_new_flats(self, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = context.job.chat_id
        filters = build_filters(context.job.data)

        flats = await execute_search(self._search_executor, filters)

        if not flats:
            return

        messages = create_flat_messages(flats)
        for message in messages:
            await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")

    @staticmethod
    def _remove_existing_jobs(context: ContextTypes.DEFAULT_TYPE, chat_id: int) -> None:
        for job in context.job_queue.get_jobs_by_name(str(chat_id)):
            job.schedule_removal()