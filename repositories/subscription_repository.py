from data_base.data_base import get_session
from data_base.models.subscriptions_model import Subscription


class SubscriptionRepository:
    
    def save(self, subscription: Subscription) -> None:
        with get_session() as session:
            session.add(subscription)

    def get_by_user_id(self, telegram_user_id: int) -> Subscription | None:
        with get_session() as session:
            return (
                session.query(Subscription)
                .filter_by(telegram_user_id=telegram_user_id)
                .first()
            )

    def remove_by_user_id(self, telegram_user_id: int) -> None:
        with get_session() as session:
            (
                session.query(Subscription)
                .filter_by(telegram_user_id=telegram_user_id)
                .delete()
            )