from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from pages.components.button import Button
from pages.components.flat_components.flats import Flats
from pages.components.input_field import InputField
from pages.components.pagination import Pagination
from pages.components.selector import Selector


class MainPage(BasePage):
    min_price_input = InputField(By.ID, 'From2')
    max_price_input = InputField(By.ID, 'To3')
    min_square_input = InputField(By.ID, 'From5')
    max_square_input = InputField(By.ID, 'To6')
    min_rooms_selector = Selector(By.CSS_SELECTOR, 'select[data-facet-type="select-box-from"]')
    max_rooms_selector = Selector(By.CSS_SELECTOR, 'select[data-facet-type="select-box-to"]')
    search_button = Button(By.CSS_SELECTOR, '.btn-main.refresh-display')
    
    def __init__(self, driver: WebDriver, url: str):
        super().__init__(driver, url)
        self._pagination = Pagination(self._driver)
        self._flats = Flats(self._driver)
    
    @property
    def pagination(self) -> Pagination:
        return self._pagination
    
    @property
    def flats(self) -> Flats:
        return self._flats

    def set_filters(
            self,
            min_price: str,
            max_price: str,
            min_square: str,
            max_square: str,
            min_rooms: str,
            max_rooms: str,
    ):
        self.min_price_input.enter_text(min_price)
        self.max_price_input.enter_text(max_price)
        self.min_square_input.enter_text(min_square)
        self.max_square_input.enter_text(max_square)
        self.min_rooms_selector.set_element_from_selector_by_text(min_rooms, wait_before=1)
        self.max_rooms_selector.set_element_from_selector_by_text(max_rooms, wait_before=1)
        self.search_button.click_by_first_visible()
        self.refresh()
