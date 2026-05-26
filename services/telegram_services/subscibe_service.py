import asyncio

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from data_base.models.subscriptions_model import Subscription
from pages.components.flat_components.flat import Flat
from repositories.seen_flat_repository import SeenFlatRepository
from repositories.subscription_repository import SubscriptionRepository
from services.search_executor import SearchExecutor
from services.search_filters import SearchFilters
from services.telegram_services.telegram_search_utils import (
    build_filters,
    try_create_flat_messages,
    get_missing_filter_fields, build_filters_from_model, convert_to_model,
)


class SubscribeService:
    def __init__(self,
                 search_executor: SearchExecutor,
                 app: Application,
                 flats_repo: SeenFlatRepository,
                 subscribe_repo: SubscriptionRepository
                 ) -> None:
        self._flats_repo = flats_repo
        self._subscribe_repo = subscribe_repo
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
                "Firstly choose filter by using /search.\n"
                f"Not enough field: {', '.join(missing_fields)}"
            )
            return

        self._remove_existing_jobs(context, chat_id)
        subscription = Subscription.from_filters(
            telegram_user_id=chat_id,
            chat_id=update.effective_user.id,
            filters=build_filters(context.user_data)
        )
        self._subscribe_repo.save(subscription)
        context.job_queue.run_repeating(
            callback=self._send_new_flats,
            interval=60,
            first=10,
            chat_id=chat_id,
            name=str(chat_id),
        )
        await update.message.reply_text("Подписка включена.")

    async def _unsubscribe(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.effective_chat.id
        jobs = context.job_queue.get_jobs_by_name(str(chat_id))

        if not jobs:
            await update.message.reply_text("Активной подписки нет.")
            return

        self._remove_existing_jobs(context, chat_id)
        self._subscribe_repo.remove_by_user_id(telegram_user_id=update.effective_user.id)
        self._flats_repo.remove_by_user_id(telegram_user_id=chat_id)
        await update.message.reply_text("Подписка отключена.")

    async def _send_new_flats(self, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = context.job.chat_id
        user_id = context.job.user_id
        subscribe_model = self._subscribe_repo.get_by_user_id(telegram_user_id=user_id)
        if not subscribe_model:
            raise RuntimeError('Subscription not found')

        filters = build_filters_from_model(subscribe_model)
        new_flats = self._select_new_flats(filters=filters, user_id=user_id)
        messages = try_create_flat_messages(flats=new_flats, error_message='There is no new flats today')

        for message in messages:
            await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
        self._flats_repo.save_all(convert_to_model(new_flats, user_id))

    async def _select_new_flats(self, filters: SearchFilters, user_id: int) -> list[Flat]:
        all_flats = await asyncio.to_thread(self._search_executor.execute, filters)
        seen_flat = self._flats_repo.get_by_user_id(telegram_user_id=user_id)
        seen_flats_ids = {flat.id for flat in seen_flat}
        return [flat for flat in all_flats if flat.id not in seen_flats_ids]

    def _remove_existing_jobs(self, context: ContextTypes.DEFAULT_TYPE, chat_id: int) -> None:
        for job in context.job_queue.get_jobs_by_name(str(chat_id)):
            job.schedule_removal()