import json
import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

import data_base.data_base as db
from configs.config import Config
from data_base.models.base import Base
from services.flats.search_executor import SearchExecutor
from webdriver.driver_manager import DriverManager


@pytest.fixture
def search_executor() -> SearchExecutor:
    driver_manager = DriverManager(config=Config.SELENIUM)
    return SearchExecutor(config=Config.SELENIUM, driver_manager=driver_manager)
    

@pytest.fixture
def fresh_db():
    load_dotenv()
    db_url = os.getenv('test_db_url')
    if db_url is None:
        raise Exception('No db_url for database')
    db.init_db(db_url)
    Base.metadata.drop_all(bind=db.Engine)
    Base.metadata.create_all(bind=db.Engine)
