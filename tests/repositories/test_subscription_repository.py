import allure
import pytest

from repositories.subscription_repository import SubscriptionRepository
from tests.data_factories import make_subscription


@pytest.mark.usefixtures('fresh_db')
class TestSubscriptionRepository:

    def test_save_subscription(self) -> None:
        test_id = 12
        repo = SubscriptionRepository()

        with allure.step('Prepare subscription'):
            expected_subscription = make_subscription(user_id=test_id, )

        with allure.step('Save subscription'):
            repo.save(expected_subscription)

        with allure.step('Get subscription by user_id'):
            actual_subscription = repo.get_by_user_id(telegram_user_id=test_id, )

        with allure.step('Verify saved subscription'):
            assert actual_subscription is not None, (
                f'Subscription for user_id={test_id} was not found after save')
            assert actual_subscription.telegram_user_id == expected_subscription.telegram_user_id, (
                f'Expected user_id={expected_subscription.telegram_user_id}, '
                f'got {actual_subscription.telegram_user_id}')
            assert actual_subscription.rooms_type == expected_subscription.rooms_type, (
                f'Expected rooms_type={expected_subscription.rooms_type}, '
                f'got {actual_subscription.rooms_type}')
            assert actual_subscription.min_price == expected_subscription.min_price, (
                f'Expected min_price={expected_subscription.min_price}, '
                f'got {actual_subscription.min_price}')
            assert actual_subscription.max_price == expected_subscription.max_price, (
                f'Expected max_price={expected_subscription.max_price}, '
                f'got {actual_subscription.max_price}')

    def test_remove_subscription_by_user_id(self) -> None:
        test_id = 12
        repo = SubscriptionRepository()

        with allure.step('Prepare subscription'):
            expected_subscription = make_subscription(user_id=test_id, )

        with allure.step('Save subscription'):
            repo.save(expected_subscription)

        with allure.step('Remove subscription by user_id'):
            repo.remove_by_user_id(telegram_user_id=test_id, )

        with allure.step('Verify subscription was removed'):
            result = repo.get_by_user_id(telegram_user_id=test_id, )
            assert result is None, (f'Subscription for user_id={test_id} still exists after remove')

    def test_get_all_subscriptions(self) -> None:
        first_test_id = 1
        second_test_id = 2
        repo = SubscriptionRepository()

        with allure.step('Prepare subscriptions'):
            first_subscription = make_subscription(user_id=first_test_id, )
            second_subscription = make_subscription(user_id=second_test_id, )

        with allure.step('Save subscriptions'):
            repo.save(first_subscription)
            repo.save(second_subscription)

        with allure.step('Get all subscriptions'):
            subscriptions = repo.get_all()

        with allure.step('Verify all subscriptions were returned'):
            actual_ids = {subscription.telegram_user_id for subscription in subscriptions}
            assert actual_ids == {first_test_id, second_test_id}, (
                f'Expected subscriptions for users '
                f'{first_test_id} and {second_test_id}, '
                f'got {actual_ids}')
