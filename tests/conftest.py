import json
from pathlib import Path

import pytest

from services.search_filters import SearchFilters
from webdriver.driver_manager import DriverManager


@pytest.fixture(scope='session')
def setup() -> tuple[DriverManager, dict]:
    path = Path(__file__).parents[1] / "config/test_config.json"
    with path.open(encoding="utf-8") as file:
        config = json.load(file)
    driver_manager = DriverManager(config=config)
    yield driver_manager, config

@pytest.fixture(scope='session')
def test_filter():
    return SearchFilters(min_price='10', max_price='200', min_square='10', max_square='30', rooms_count='1')
