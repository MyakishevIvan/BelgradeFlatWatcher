from telegram.ext import ApplicationBuilder
from services.search_executor import SearchExecutor
from services.telegram_services.dialog_service import DialogService
from services.telegram_services.subscibe_service import SubscribeService


class FlatBot:
    def __init__(self, token: str, search_executor: SearchExecutor):
        self._app = ApplicationBuilder().token(token).build()
        self._dialog_service = DialogService(app=self._app, search_executor=search_executor)
        self._subscribe_service = SubscribeService(app=self._app, search_service=search_executor)
        self._register_handlers()

    def _register_handlers(self):
        self._dialog_service.register_handlers()
        self._subscribe_service.register_handlers()

    def run(self):
        self._app.run_polling()
