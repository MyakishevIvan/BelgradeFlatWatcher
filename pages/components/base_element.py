import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BaseElement:
    def __init__(self, *locator: str):
        self._locator = locator
        self._driver: WebDriver = None
        self._waiter: WebDriverWait = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.__class__(*self._locator)._bind(instance._driver)

    def _bind(self, driver: WebDriver):
        self._driver = driver
        self._waiter = WebDriverWait(driver, 10)
        return self

    def wait_visible(self) -> WebElement:
        return self._waiter.until(EC.visibility_of_element_located(self._locator))

    def wait_presence_all(self) -> list[WebElement]:
        return self._waiter.until(EC.presence_of_all_elements_located(self._locator))

    def click(self, wait_before: int | None = None, wait_after: int | None = None, index: int = 0) -> None:
        if wait_before:
            time.sleep(wait_before)
        elements = self.wait_presence_all()
        if index >= len(elements):
            raise IndexError(f"Index of element {index} out of bounds."
                             f" Must be less than {len(elements)}")
        element = elements[index]
        self._waiter.until(
            lambda d: element.is_displayed() and element.is_enabled()
        )
        element.click()
        if wait_after:
            time.sleep(wait_after)

    def click_by_first_visible(self) -> None:
        visible_elements = [e for e in self.wait_presence_all() if e.is_displayed() and e.is_enabled()]
        if not visible_elements:
            raise RuntimeError(f"No visible elements found.")
        visible_elements[0].click()
