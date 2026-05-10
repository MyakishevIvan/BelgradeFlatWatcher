import json
import os
from pathlib import Path

from dotenv import load_dotenv

from services.search_executor import SearchExecutor
from services.search_service import SearchService
from services.telegram_services.flat_bot import FlatBot
from webdriver.driver_manager import DriverManager

if __name__ == '__main__':
    with open(Path('config/config.json'), 'r') as file:
        config = json.load(file)
    load_dotenv()
    token = os.getenv('tg_token')
    if token is None:
        raise Exception('No token for telegram bot')
    driver_manager = DriverManager(config=config)
    search_executor = SearchExecutor(config=config, driver_manager=driver_manager)
    flat_bot = FlatBot(token = token, search_executor=search_executor)
    flat_bot.run()
