from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from pages.components.flat_components.flat import Flat
from pages.components.flat_components.flat_component import FlatComponent


class Flats:
    apartments_selector = (By.CSS_SELECTOR, ".col-md-12.col-sm-12.col-xs-12.col-lg-12:not(.banner-list-item)")

    def __init__(self, driver: WebDriver):
        self._driver = driver
    
    def get_all_flats_in_page(self) -> list[Flat]:
        flats = []
        elements = self._driver.find_elements(*self.apartments_selector)
        for element in elements:
            component = FlatComponent(element)
            flat = Flat(
                id=component.get_id(),
                url=component.get_url(),
                name = component.get_name(),
                price = component.get_price(),
                square = component.get_square(),
                publication_date = component.get_publication_date(),
            )
            flats.append(flat)
        return flats        