import allure
import pytest

from repositories.seen_flat_repository import SeenFlatRepository
from tests.data_factories import make_seen_flat


@pytest.mark.usefixtures('fresh_db')
class TestSeenFlatRepository:

    def test_save_flats(self) -> None:
        test_id = 1
        repo = SeenFlatRepository()

        with allure.step('Prepare seen flat'):
            expected_flat = make_seen_flat(user_id=test_id, )

        with allure.step('Save flat'):
            repo.save_all([expected_flat])

        with allure.step('Get flats by user_id'):
            actual_flat_list = repo.get_by_user_id(telegram_user_id=test_id, )

        with allure.step('Verify saved flat'):
            assert len(actual_flat_list) == 1, (
                f'Expected 1 saved flat for user_id={test_id}, '
                f'got {len(actual_flat_list)}')
            actual_flat = actual_flat_list[0]
            assert actual_flat.telegram_user_id == expected_flat.telegram_user_id, (
                f'Expected user_id={expected_flat.telegram_user_id}, '
                f'got {actual_flat.telegram_user_id}')
            assert actual_flat.flat_id == expected_flat.flat_id, (
                f'Expected flat_id={expected_flat.flat_id}, '
                f'got {actual_flat.flat_id}')
            assert actual_flat.flat_url == expected_flat.flat_url, (
                f'Expected flat_url={expected_flat.flat_url}, '
                f'got {actual_flat.flat_url}')

    def test_remove_flats_by_user_id(self) -> None:
        user_id = 1
        repo = SeenFlatRepository()

        with allure.step('Prepare seen flat'):
            seen_flat = make_seen_flat(user_id=user_id, )

        with allure.step('Save flat'):
            repo.save_all([seen_flat])

        with allure.step('Remove flats by user_id'):
            repo.remove_by_user_id(telegram_user_id=user_id, )

        with allure.step('Verify flats were removed'):
            result = repo.get_by_user_id(telegram_user_id=user_id, )
            assert result == [], f'Flats for user_id={user_id} still exist after remove'
