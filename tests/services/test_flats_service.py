import allure
import pytest

from repositories.seen_flat_repository import SeenFlatRepository
from repositories.subscription_repository import SubscriptionRepository
from services.flats.flats_service import FlatsService
from services.telegram.telegram_search_utils import build_filters
from tests.data_factories import make_subscription, make_seen_flat, make_flat


@pytest.mark.usefixtures('fresh_db')
class TestFlatsService:

    @pytest.mark.asyncio
    async def test_search_new_flats_returns_only_unseen_flats(self, mocker) -> None:
        user_id = 1
        seen_flat_id = 1
        new_flat_id = 2

        with allure.step('Prepare subscription and seen flats'):
            subscription = make_subscription(user_id=user_id)
            seen_flat = make_seen_flat(user_id=user_id, flat_id=seen_flat_id)

        with allure.step('Prepare search results'):
            old_flat = make_flat(flat_id=seen_flat_id)
            new_flat = make_flat(flat_id=new_flat_id)

        with allure.step('Mock search executor'):
            search_executor = mocker.Mock()
            search_executor.execute.return_value = [old_flat, new_flat]

        with allure.step('Create service and save test data'):
            service = FlatsService(search_executor, SeenFlatRepository(), SubscriptionRepository())
            service.save_subscription(subscription)
            service.save_flats([seen_flat])

        with allure.step('Search new flats'):
            actual_flats = await service.search_new_flats(user_id=user_id)

        with allure.step('Verify only unseen flat is returned'):
            assert len(actual_flats) == 1, (
                f'Expected 1 new flat with flat_id={new_flat.id}, '
                f'got flats count={len(actual_flats)}')
            actual_flat = actual_flats[0]
            assert actual_flat.id == new_flat.id, (
                f'Expected new flat with flat_id={new_flat.id}, '
                f'got flat_id={actual_flat.id}')

        with allure.step('Search new flats gives empty list without new flats'):
            actual_flats = await service.search_new_flats(user_id=user_id)
            assert len(actual_flats) == 0, f'Expected no new flats, got {len(actual_flats)} flats'

    @pytest.mark.asyncio
    async def test_search_raises_when_subscription_not_found(self, mocker) -> None:
        user_id = 1

        with allure.step('Mock search executor'):
            search_executor = mocker.Mock()
            search_executor.execute.return_value = [make_flat(flat_id=1)]

        with allure.step('Create service without subscription'):
            service = FlatsService(search_executor, SeenFlatRepository(), SubscriptionRepository())

        with allure.step('Verify exception is raised'):
            with pytest.raises(RuntimeError, match='Subscription not found'):
                await service.search_new_flats(user_id=user_id)

    def test_build_filters_raises_when_required_field_missing(self) -> None:
        with allure.step('Prepare filter data'):
            data = {
                'min_price': 100,
                'max_price': 500,
            }

        with allure.step('Raise when required fields are missing'):
            with pytest.raises(
                    ValueError,
                    match='Missing fields',
            ):
                build_filters(data)

    def test_remove_user_data_removes_all_user_data(self, mocker) -> None:
        user_id = 1
        with allure.step('Prepare subscription and seen flats'):
            subscription = make_subscription(user_id=user_id)
            flat = make_seen_flat(user_id=user_id, flat_id=1)

        with allure.step('Create service and save test data'):
            search_executor = mocker.Mock()
            service = FlatsService(search_executor, SeenFlatRepository(), SubscriptionRepository())
            service.save_subscription(subscription)
            service.save_flats([flat])

        with allure.step('Remove user data'):
            service.remove_user_data(user_id=user_id)

        with allure.step('Verify user data is removed'):
            flats = service.get_user_flats(user_id=user_id)
            subscriptions = service.get_all_subscriptions()
            assert flats == [], (
                f'Expected no flats for user_id={user_id}, '
                f'got {len(flats)} flats'
            )
            assert subscriptions == [], (
                f'Expected no subscriptions for user_id={user_id}, '
                f'got {len(subscriptions)} subscriptions'
            )
