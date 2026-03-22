from datetime import date, datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class FlatComponent:
    square_locator = (By.CSS_SELECTOR, ".product-features li")
    square_wrapper_locator = (By.CSS_SELECTOR, ".value-wrapper")
    price_locator = (By.CSS_SELECTOR, ".central-feature")
    header_locator = (By.CSS_SELECTOR, "h3.product-title a")
    location_locator = (By.CSS_SELECTOR, "ul.subtitle-places")
    date_locator = (By.CSS_SELECTOR, ".publish-date")

    def __init__(self, web_element: WebElement):
        self._web_element = web_element

    def get_square(self) -> str:
        elements = self._web_element.find_elements(*self.square_locator)
        if not elements:
            raise ValueError("Square element not found")

        first_element = elements[0]
        square_text = first_element.find_element(*self.square_wrapper_locator).text.strip()
        parts = square_text.split()
        if not parts:
            raise ValueError("Square text is empty")

        return parts[0]

    def get_price(self) -> str:
        price_text = self._web_element.find_element(*self.price_locator).text.strip()
        parts = price_text.split()
        if not parts:
            raise ValueError("Price text is empty")

        return parts[0]

    def get_url(self) -> str:
        header = self._web_element.find_element(*self.header_locator)
        url = header.get_attribute("href")
        if not url:
            raise ValueError("URL not found")

        return url

    def get_name(self) -> str:
        name = self._web_element.find_element(*self.header_locator).text.strip()
        if not name:
            raise ValueError("Name is empty")

        return name

    def get_location(self) -> str:
        location_element = self._web_element.find_element(*self.location_locator)
        items = location_element.find_elements(By.TAG_NAME, "li")
        if len(items) < 2:
            raise ValueError("Location item not found")

        raw_text_location = items[1].text.strip()
        parts = raw_text_location.split()
        if len(parts) < 2:
            raise ValueError(f"Unexpected location format: {raw_text_location}")

        return parts[1]

    def get_publication_date(self) -> date:
        raw_result = self._web_element.find_element(*self.date_locator).text.strip()

        if raw_result.endswith("."):
            raw_result = raw_result[:-1]

        return datetime.strptime(raw_result, "%d.%m.%Y").date()