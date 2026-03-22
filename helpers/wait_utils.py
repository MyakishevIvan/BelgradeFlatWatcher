import time
from typing import Callable, TypeVar

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

T = TypeVar("T")


class WaitUtils:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self._wait = WebDriverWait(driver, timeout)

    def wait(self, method: Callable, message: str = "", wait_before: int | None = None) -> T:
        if wait_before:
            time.sleep(wait_before)

        return self._wait.until(method, message)
