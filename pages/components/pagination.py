from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from pages.components.button import Button


class Pagination:
    pages_locator = (By.CSS_SELECTOR, "#pager-1 a.page-link")
    next_page_button = Button(By.CSS_SELECTOR, ".page-link.next")

    def __init__(self, driver: WebDriver):
            self._driver = driver
    
    def get_pages_list(self) ->list[WebElement]:
        pages = self._driver.find_elements(*self.pages_locator)
        elements = [p for p in pages if p.text.isdigit()]
        return elements
    
    def get_last_page_number(self):
        numbers = [int(p.text) for p in self.get_pages_list()]
        return max(numbers)
