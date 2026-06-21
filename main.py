import os

from dotenv import load_dotenv

from configs.config import Config
from configs.logging_config import setup_logging
from data_base.data_base import init_db
from repositories.seen_flat_repository import SeenFlatRepository
from repositories.subscription_repository import SubscriptionRepository
from services.flats.flats_service import FlatsService
from services.flats.search_executor import SearchExecutor
from services.telegram.telegram_application import TelegramApplication
from webdriver.driver_manager import DriverManager

if __name__ == '__main__':
    config = Config.SELENIUM
    load_dotenv()
    setup_logging()
    token = os.getenv('tg_token')
    if token is None:
        raise Exception('No token for telegram bot')

    db_url = os.getenv('db_url')
    if db_url is None:
        raise Exception('No db_url for database')
    
    init_db(db_url=db_url)
    flats_repo = SeenFlatRepository()
    subscribe_repo = SubscriptionRepository()
    driver_manager = DriverManager(config=Config.SELENIUM)
    search_executor = SearchExecutor(config=Config.SELENIUM, driver_manager=driver_manager)
    service = FlatsService(search_executor=search_executor, flats_repo=flats_repo,
                           subscribe_repo=subscribe_repo)
    app = TelegramApplication(token=token, flats_service=service)
    app.run()
