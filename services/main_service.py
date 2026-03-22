from typing import Dict

from selenium import webdriver

from pages.components.flat_components.flat import Flat
from pages.main_page import MainPage


class MainService:
    def __init__(self, driver: webdriver, config: Dict) -> None:
        self._driver = driver
        self.main_page = MainPage(driver=self._driver, url=config.get('url'))

    def get_all_flats(self) -> list[Flat]:
        flats_list = []
        self.main_page.open()
        self.main_page.set_filters(
            min_price='10',
            max_price='250',
            min_square='10',
            max_square='40',
            min_rooms='1.0',
            max_rooms='2.0'
        )
        number = self.main_page.pagination.get_last_page_number()
        for i in range(number):
            flats = self.main_page.flats.get_all_flats_in_page()
            flats_list.extend(flats)
            if i < number - 1:
                self.main_page.pagination.next_page_button.click(wait_after=3)
