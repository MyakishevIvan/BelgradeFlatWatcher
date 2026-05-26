from telegram.ext import ApplicationBuilder

from repositories.seen_flat_repository import SeenFlatRepository
from services.search_executor import SearchExecutor
from services.telegram_services.dialog_service import DialogService
from services.telegram_services.subscibe_service import SubscribeService


class FlatBot:
    def __init__(self, token: str,
                 search_executor: SearchExecutor,
                 flat_repo: SeenFlatRepository,
                 subscribe_repo: SubscribeService):
        self._app = ApplicationBuilder().token(token).build()
        self._dialog_service = DialogService(
            app=self._app,
            search_executor=search_executor,
            flats_repo=flat_repo
        )
        self._subscribe_service = SubscribeService(
            app=self._app,
            search_executor=search_executor,
            subscribe_repo=subscribe_repo,
            flats_repo=flat_repo
        )
        self._register_handlers()

    def _register_handlers(self):
        self._dialog_service.register_handlers()
        self._subscribe_service.register_handlers()
        self._subscribe_service.restore_subscription_jobs()
        
    def run(self):
        self._app.run_polling()
