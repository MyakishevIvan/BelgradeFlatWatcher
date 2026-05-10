from contextlib import contextmanager
from typing import Dict, Iterator

from selenium.webdriver.remote.webdriver import WebDriver

from webdriver.driver_factory import DriverFactory


class DriverManager:
    def __init__(self, config: Dict) -> None:
        self._factory = DriverFactory(config)
        self._driver: WebDriver | None = None
        
    @contextmanager
    def driver_session(self) -> Iterator[WebDriver]:
        driver = self._factory.init_driver()
        try:
            yield driver
        finally:
            driver.quit()