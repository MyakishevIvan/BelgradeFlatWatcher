from telegram import Update
from telegram.ext import ContextTypes, JobQueue

from data_base.models.subscriptions_model import Subscription


class SubscriptionHandler:

    def __init__(self, job_queue: JobQueue):
        self._job_queue = job_queue
        
    async def subscribe_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback) -> None:
        chat_id = update.effective_chat.id
        self._remove_existing_jobs(context, chat_id)
        context.job_queue.run_repeating(
            callback=callback,
            interval=60,
            first=10,
            chat_id=chat_id,
            user_id=update.effective_user.id,
            name=str(chat_id),
        )
        await update.message.reply_text("Subscription enabled.")

    def restore_subscription_jobs(self, subscriptions: list[Subscription], callback) -> None:
        for subscription in subscriptions:
            self._job_queue.run_repeating(
                callback=callback,
                interval=60,
                first=10,
                chat_id=subscription.chat_id,
                user_id=subscription.telegram_user_id,
                name=str(subscription.chat_id),
            )

    async def unsubscribe_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.effective_chat.id
        jobs = context.job_queue.get_jobs_by_name(str(chat_id))
        if not jobs:
            await update.message.reply_text("There is no active subscription.")
            return
        self._remove_existing_jobs(context, chat_id)
        await update.message.reply_text("Subscription disabled.")

    def _remove_existing_jobs(self, context: ContextTypes.DEFAULT_TYPE, chat_id: int) -> None:
        for job in context.job_queue.get_jobs_by_name(str(chat_id)):
            job.schedule_removal()
