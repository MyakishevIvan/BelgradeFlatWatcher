import allure

from configs.config import Config
from services.telegram.telegram_search_utils import try_create_flat_messages
from tests.data_factories import make_flats_list


def test_messages_returns_error_string_for_empty_result() -> None:
    expected_message = ['Flats not found']

    with allure.step('Create message for empty flats list'):
        actual_message = try_create_flat_messages([])

    with allure.step('Verify error message'):
        assert actual_message == expected_message, (
            f'Expected message={expected_message[0]}, '
            f'got message={actual_message}'
        )


def test_create_flat_messages_splits_messages_by_telegram_limit() -> None:
    limit = Config.SEARCH['CHAR_LIMIT']
    flats = make_flats_list()

    with allure.step('Create messages from flats list'):
        messages = try_create_flat_messages(flats)

    with allure.step('Verify every message fits Telegram limit'):
        for message in messages:
            assert len(message) <= limit, (
                f'Expected message length <= {limit}, '
                f'got {len(message)}'
            )