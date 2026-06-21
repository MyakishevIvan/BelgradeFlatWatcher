import allure

from services.flats.search_executor import SearchExecutor
from tests.data_factories import make_filter
from tests.heplers import to_float


def test_search_executor_returns_flats_by_filters(search_executor: SearchExecutor) -> None:
    with allure.step('Prepare filter'):
        filters = make_filter()

    with allure.step('Execute flats search'):
        flats = search_executor.execute(filters)

    with allure.step('Search result should be received by filter'):
        assert flats, 'Flats list should not be empty'
        for flat in flats:
            assert int(filters.max_price) >= int(flat.price) >= int(filters.min_price), (
                f'Price={flat.price} should be between {filter.min_price} and {filters.max_price}'
            )
            assert to_float(filters.max_square) >= to_float(flat.square) >= to_float(filters.min_square), (
                f'Square={flat.square} should be between {filters.min_square} '
                f'and {filters.max_square}'
            )
