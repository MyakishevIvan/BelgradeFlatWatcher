from pages.components.base_element import BaseElement


class Button(BaseElement):
    def __init__(self, by: str, value: str):
        super().__init__(by, value)
