import json
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

import data_base.data_base as db
from data_base.models.base import Base
from services.flats.search_filters import SearchFilters
from webdriver.driver_manager import DriverManager


@pytest.fixture
def setup() -> tuple[DriverManager, dict]:
    path = Path(__file__).parents[1] / "configs/test_selenium_config.json"
    with path.open(encoding="utf-8") as file:
        config = json.load(file)
    driver_manager = DriverManager(config=config)
    yield driver_manager, config

@pytest.fixture
def test_filter():
    return SearchFilters(min_price='10', max_price='200', min_square='10', max_square='30', rooms_type='1')

@pytest.fixture
def fresh_db():
    load_dotenv()
    db_url = os.getenv('test_db_url')
    if db_url is None:
        raise Exception('No db_url for database')
    db.init_db(db_url)
    Base.metadata.drop_all(bind=db.Engine)
    Base.metadata.create_all(bind=db.Engine)