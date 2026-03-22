import time

from pages.components.base_element import BaseElement


class InputField(BaseElement):
    def __init__(self, by: str, value: str):
        super().__init__(by, value)

    def enter_text(self, text: str, wait_before: int | None = None):
        if wait_before:
            time.sleep(wait_before)
        self.wait_visible().send_keys(text)
