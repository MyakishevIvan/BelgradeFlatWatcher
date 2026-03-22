from selenium.webdriver.remote.webdriver import WebDriver


class BaseComponent:
    def __init__(self, driver: WebDriver):
        self._driver = driver