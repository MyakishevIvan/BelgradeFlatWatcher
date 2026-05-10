from typing import Dict

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver


class DriverFactory:
    def __init__(self, config: Dict) -> None:
        self._config = config

    def init_driver(self) -> WebDriver:
        match self._config.get("browser"):
            case "chrome":
                chrome_options = ChromeOptions()
                if self._config.get('headless'):
                    chrome_options.add_argument("--headless=new")
                chrome_options.add_argument(f"--window-size={self._config.get('resolution')}")
                chrome_options.add_experimental_option("detach", self._config.get('detach'))
                return ChromeDriver(options=chrome_options)
            case "firefox":
                firefox_options = FirefoxOptions()
                if self._config.get('headless'):
                    firefox_options.add_argument("-headless")
                width, height = self._config.get("resolution").split(",")
                firefox_driver = FirefoxDriver(options=firefox_options)
                firefox_driver.set_window_size(width, height)
                return firefox_driver
            case _:
                raise ValueError("Unsupported browser")
