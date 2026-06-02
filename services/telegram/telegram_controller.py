from telegram.ext import ConversationHandler, ContextTypes

from data_base.models.subscriptions_model import Subscription
from enums.conversation_type import ConversationType
from services.flats.flats_service import FlatsService
from services.telegram.dialog_handler import DialogHandler
from services.telegram.subscription_handler import SubscriptionHandler
from services.telegram.telegram_search_utils import build_filters, convert_to_model, try_create_flat_messages


class TelegramController:
    def __init__(self,
            flats_service: FlatsService,
            dialog_handler: DialogHandler,
            subscription_handler: SubscriptionHandler
    ):
        self._flats_service = flats_service
        self._dialog_handler = dialog_handler
        self._subscription_handler = subscription_handler

    async def start(self, update, context) -> int:
        await self._dialog_handler.start(update, context)
        return ConversationType.ROOMS

    async def handle_rooms(self, update, context) -> int:
        await self._dialog_handler.handle_rooms(update, context)
        return ConversationType.PRICE

    async def handle_price(self, update, context) -> int:
        await self._dialog_handler.handle_price(update, context)
        return ConversationType.SQUARE

    async def handle_square(self, update, context) -> int:
        await self._dialog_handler.handle_square(update, context)
        return ConversationType.SEARCH

    async def subscribe(self, update, context):
        subscription = Subscription.from_filters(
            telegram_user_id=update.effective_user.id,
            chat_id=update.effective_chat.id,
            filters=build_filters(context.user_data)
        )
        self._flats_service.save_subscriptions(subscription)
        await self._subscription_handler.subscribe_handler(update, context, self._send_new_flats)

    async def unsubscribe(self, update, context):
        self._flats_service.remove_user_data(user_id=update.effective_user.id)
        await self._subscription_handler.unsubscribe_handler(update, context)

    async def search(self, update, context) -> int:
        await self._dialog_handler.handle_search(update, context)
        user_id = update.effective_user.id
        filters = build_filters(context.user_data)
        flats = await self._flats_service.search_by_filters(filters)

        for message in try_create_flat_messages(flats):
            await update.callback_query.message.reply_text(message, parse_mode="HTML")
        await update.callback_query.message.reply_text('You can use /subscribe to receive updates once in a day',
                                                       parse_mode="HTML")
        self._flats_service.save_flats(convert_to_model(flats, user_id))
        return ConversationHandler.END

    def restore_subscription_jobs(self) -> None:
        subscriptions = self._flats_service.get_all_subscriptions()
        self._subscription_handler.restore_subscription_jobs(subscriptions, self._send_new_flats)
        
    async def _send_new_flats(self, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = context.job.chat_id
        user_id = context.job.user_id

        try:
            new_flats = await self._flats_service.search_new_flats(user_id=user_id)
        except RuntimeError as e:
            await context.bot.send_message(chat_id=chat_id, text=str(e))
            return

        messages = try_create_flat_messages(flats=new_flats, error_message='There is no new flats today')
        for message in messages:
            await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
