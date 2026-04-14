import json
from pathlib import Path

from services.search_filters import SearchFilters
from webdriver.driver_factory import DriverFactory
from services.search_service import SearchService


def test_page_filter():
    path = Path(__file__).parents[1] / "config/test_config.json" 
    with path.open(encoding="utf-8") as file:
        config = json.load(file)
    driver_factory = DriverFactory(config=config)
    driver = driver_factory.init_driver()
    search_service = SearchService(driver=driver, config=config)
    filters = SearchFilters(min_price='10', max_price='1700', min_square='10', max_square='1000', rooms_count='2')
    flats = search_service.get_all_flats(filters=filters)
    assert flats 