import json
import os
from pathlib import Path
from dotenv import load_dotenv

from services.telegram_services.flat_bot import FlatBot
from webdriver.driver_factory import DriverFactory
from services.search_service import SearchService
from services.telegram_services.dialog_service import DialogService

if __name__ == '__main__':
    with open(Path('config/config.json'), 'r') as file:
        config = json.load(file)
    load_dotenv()
    token = os.getenv('tg_token')
    if token is None:
        raise Exception('No token for telegram bot')
    driver_factory = DriverFactory(config=config)
    driver = driver_factory.init_driver()
    search_service = SearchService(driver=driver, config=config)
    flat_bot = FlatBot(token, search_service)
    flat_bot.run()
    
    