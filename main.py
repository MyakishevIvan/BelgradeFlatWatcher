import json
from pathlib import Path

from services.driver_factory import DriverFactory
from services.main_service import MainService

if __name__ == '__main__':
    with open(Path('config/config.json'), 'r') as file:
        config = json.load(file)

    driver_factory = DriverFactory(config=config)
    driver = driver_factory.init_driver()
    service = MainService(driver=driver, config=config)
    flats = service.get_all_flats()
    