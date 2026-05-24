import json
import os
from pathlib import Path

from dotenv import load_dotenv

from data_base.data_base import init_db
from repositories.seen_flat_repository import SeenFlatRepository
from repositories.subscription_repository import SubscriptionRepository
from services.search_executor import SearchExecutor
from services.telegram_services.flat_bot import FlatBot
from webdriver.driver_manager import DriverManager

if __name__ == '__main__':
    with open(Path('config/config.json'), 'r') as file:
        config = json.load(file)
    load_dotenv()
    token = os.getenv('tg_token')
    if token is None:
        raise Exception('No token for telegram bot')
    
    db_url = os.getenv('db_url')
    if db_url is None:
        raise Exception('No db_url for database')
    
    init_db(db_url=db_url)
    flats_repo = SeenFlatRepository()
    subscribe_repo = SubscriptionRepository()
    driver_manager = DriverManager(config=config)
    search_executor = SearchExecutor(config=config, driver_manager=driver_manager)
    flat_bot = FlatBot(
        token=token,
        search_executor=search_executor,
        flat_repo=flats_repo,
        subscribe_repo=subscribe_repo
    )
    flat_bot.run()
