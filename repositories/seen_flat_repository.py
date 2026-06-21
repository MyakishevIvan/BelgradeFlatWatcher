from data_base.data_base import get_session
from data_base.models.seen_flats_model import SeenFlat


class SeenFlatRepository:

    def save_all(self, flats: list[SeenFlat]) -> None:
        with get_session() as session:
            session.add_all(flats)

    def get_by_user_id(self, telegram_user_id: int) -> list[SeenFlat]:
        with get_session() as session:
            return (
                session.query(SeenFlat)
                .filter_by(telegram_user_id=telegram_user_id)
                .all()
            )

    def remove_by_user_id(self, telegram_user_id: int) -> None:
        with get_session() as session:
            (
                session.query(SeenFlat)
                .filter_by(telegram_user_id=telegram_user_id)
                .delete()
            )
