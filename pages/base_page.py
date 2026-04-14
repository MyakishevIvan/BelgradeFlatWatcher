from typing import Self

from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:
    def __init__(self, driver: WebDriver, url):
        self._driver = driver
        self._url = url
    
    @property
    def url(self) -> str:
        return self._url
    
    @url.setter
    def url(self, url: str):
        self._url = url
    
    def open(self):
        self._driver.get(self._url)
        return self
    
    def refresh(self):
        self._driver.refresh()