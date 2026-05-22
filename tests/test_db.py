from data_base.models.seen_flats_model import SeenFlat
from data_base.models.subscriptions_model import Subscription
from repositories.seen_flat_repository import SeenFlatRepository
from repositories.subscription_repository import SubscriptionRepository

def test_db(fresh_db):
    flat1 = SeenFlat(telegram_user_id=1, flat_url='test', flat_id=1)
    flat2 = SeenFlat(telegram_user_id=2, flat_url='test1', flat_id=2)
    subscription1 = Subscription(
        telegram_user_id=1,
        chat_id=1,
        min_price=100,
        max_price=200,
        min_square=10,
        max_square=100,
        rooms_count=3
    )
    subscription2 = Subscription(
        telegram_user_id=2,
        chat_id=1,
        min_price=100,
        max_price=200,
        min_square=10,
        max_square=100,
        rooms_count=3
    )
    subscription_repository = SubscriptionRepository()
    seen_flat_repository = SeenFlatRepository()
    subscription_repository.save(subscription1)
    subscription_repository.save(subscription2)
    seen_flat_repository.save(flat1)
    seen_flat_repository.save(flat2)
    actual_subscription = subscription_repository.get_by_user_id(1)
    assert actual_subscription == subscription1, 'subscription not equal'
    actual_flats_list = seen_flat_repository.get_by_user_id(1)
    assert actual_flats_list == [flat1], 'flat list not equal' 