from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer

from data_base.models.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_user_id: Mapped[int] = mapped_column(Integer)
    chat_id: Mapped[int] = mapped_column(Integer)
    min_price: Mapped[int] = mapped_column(Integer)
    max_price: Mapped[int] = mapped_column(Integer)
    min_square: Mapped[int] = mapped_column(Integer)
    max_square: Mapped[int] = mapped_column(Integer)
    rooms_count: Mapped[int] = mapped_column(Integer)

    def __eq__(self, other):
        if not isinstance(other, Subscription):
            return False
        return (
                self.telegram_user_id == other.telegram_user_id
                and self.chat_id == other.chat_id
                and self.min_price == other.min_price
                and self.max_price == other.max_price
                and self.min_square == other.min_square
                and self.max_square == other.max_square
                and self.rooms_count == other.rooms_count
        )
        
    