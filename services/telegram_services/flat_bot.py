from telegram.ext import ApplicationBuilder

from services.search_service import SearchService
from services.telegram_services.dialog_service import DialogService
from services.telegram_services.subscibe_service import SubscribeService


class FlatBot:
    def __init__(self, token: str, search_service: SearchService):
        self._search_service = search_service
        self._app = ApplicationBuilder().token(token).build()
        self._register_handlers()
        self._dialog_service = DialogService(app=self._app, search_service=self._search_service)
        self._subscribe_service = SubscribeService(app=self._app, search_service=self._search_service)

    def _register_handlers(self):
        self._dialog_service.register_handlers()
        self._subscribe_service.register_handlers()

    def run(self):
        self._app.run_polling()