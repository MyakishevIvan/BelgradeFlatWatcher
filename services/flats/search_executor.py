from pages.components.flat_components.flat import Flat
from services.flats.search_filters import SearchFilters
from services.flats.search_service import SearchService
from webdriver.driver_manager import DriverManager


class SearchExecutor:
    def __init__(self, config: dict, driver_manager: DriverManager) -> None:
        self._config = config
        self._driver_manager = driver_manager

    def execute(self, filters: SearchFilters) -> list[Flat]:
        with self._driver_manager.driver_session() as driver:
            service = SearchService(driver, self._config)
            return service.get_all_flats(filters)
