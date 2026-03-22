import time

from selenium.webdriver.support.select import Select
from pages.components.base_element import BaseElement


class Selector(BaseElement):
    def __init__(self, by: str, value: str):
        super().__init__(by, value)

    def set_element_from_selector_by_text(self, text: str, wait_before: int | None = None):
        if wait_before:
            time.sleep(wait_before)
        element = self.wait_visible()
        Select(element).select_by_visible_text(text)
