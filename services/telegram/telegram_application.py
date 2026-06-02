from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ConversationHandler

from enums.conversation_type import ConversationType
from services.flats.flats_service import FlatsService
from services.telegram.dialog_handler import DialogHandler
from services.telegram.subscription_handler import SubscriptionHandler
from services.telegram.telegram_controller import TelegramController


class TelegramApplication:
    def __init__(self, token: str, flats_service: FlatsService):
        self._app = ApplicationBuilder().token(token).build()
        self._controller = TelegramController(
            flats_service=flats_service,
            dialog_handler=DialogHandler(),
            subscription_handler=SubscriptionHandler(job_queue=self._app.job_queue),
        )
        self._register_handlers()

    def _register_handlers(self) -> None:
        conversation = ConversationHandler(
            entry_points=[CommandHandler("start", self._controller.start)],
            states={
                ConversationType.ROOMS: [CallbackQueryHandler(self._controller.handle_rooms)],
                ConversationType.PRICE: [CallbackQueryHandler(self._controller.handle_price)],
                ConversationType.SQUARE: [CallbackQueryHandler(self._controller.handle_square)],
                ConversationType.SEARCH: [CallbackQueryHandler(self._controller.search)],
            },
            fallbacks=[CommandHandler("start", self._controller.start)],
        )

        self._app.add_handler(conversation)
        self._app.add_handler(CommandHandler("subscribe", self._controller.subscribe))
        self._app.add_handler(CommandHandler("unsubscribe", self._controller.unsubscribe))

    def run(self) -> None:
        self._controller.restore_subscription_jobs()
        self._app.run_polling()