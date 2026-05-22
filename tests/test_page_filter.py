from services.search_executor import SearchExecutor
from services.search_filters import SearchFilters


def test_page_filter(setup, test_filter: SearchFilters):
    driver_manager, config = setup
    search = SearchExecutor(config=config, driver_manager=driver_manager)
    flats = search.execute(filters=test_filter)
    assert flats


def test_multiple_flats_search(setup, test_filter: SearchFilters):
    driver_manager, config = setup
    search = SearchExecutor(config=config, driver_manager=driver_manager)
    flats = search.execute(filters=test_filter)
    second_flats = search.execute(filters=test_filter)
    assert len(flats) == len(second_flats)
    