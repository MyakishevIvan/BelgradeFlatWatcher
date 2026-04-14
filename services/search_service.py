from typing import Any

from selenium.webdriver.remote.webdriver import WebDriver

from pages.components.flat_components.flat import Flat
from pages.main_page import MainPage
from services.search_filters import SearchFilters


class SearchService:
    def __init__(self, driver: WebDriver, config: dict[str, Any]) -> None:
        self._driver = driver
        self._base_url = config["base_url"]
        self._use_templates = config["use_templates"]
        self._url_template = config["url_template"]
        self._main_page = MainPage(driver=self._driver, url=self._base_url)

    def get_all_flats(self, filters: SearchFilters) -> list[Flat]:
        flats_list: list[Flat] = []
        if self._use_templates:
            self._open_with_template_filters(filters)
        else:
            self._open_with_ui_filters(filters)
        pages_count = self._main_page.pagination.get_last_page_number()
        for i in range(pages_count):
            flats = self._main_page.flats.get_all_flats_in_page()
            flats_list.extend(flats)
            if i < pages_count - 1:
                self._main_page.pagination.next_page_button.click(wait_after=3)
        return flats_list

    def _open_with_template_filters(self, filters: SearchFilters) -> None:
        self._main_page.url = self._build_search_url(filters)
        self._main_page.open()
        self._main_page.continue_button.try_click_by_first_visible()

    def _open_with_ui_filters(self, filters: SearchFilters) -> None:
            self._main_page.url = self._base_url
            self._main_page.open()
            self._main_page.continue_button.try_click_by_first_visible()
            self._main_page.set_filters(
                min_price=filters.min_price,
                max_price=filters.max_price,
                min_square=filters.min_square,
                max_square=filters.max_square,
                min_rooms=f"{filters.rooms_count}.0",
                max_rooms=f"{filters.rooms_count}.0",
            )

    def _build_search_url(self, filters: SearchFilters) -> str:
        return self._base_url + self._url_template.format(
            room_type=filters.room_type,
            min_price=filters.min_price,
            max_price=filters.max_price,
            min_square=filters.min_square,
            max_square=filters.max_square
        )
