from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from data_base.models.base import Base
from services.search_filters import SearchFilters


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_user_id: Mapped[int] = mapped_column(Integer)
    chat_id: Mapped[int] = mapped_column(Integer)
    min_price: Mapped[int] = mapped_column(Integer)
    max_price: Mapped[int] = mapped_column(Integer)
    min_square: Mapped[int] = mapped_column(Integer)
    max_square: Mapped[int] = mapped_column(Integer)
    rooms_type: Mapped[int] = mapped_column(String)
    
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
                and self.rooms_type == other.rooms_type
        )

    @classmethod
    def from_filters(
            cls,
            telegram_user_id: int,
            chat_id: int,
            filters: SearchFilters,
    ) -> "Subscription":
        return cls(
            telegram_user_id=telegram_user_id,
            chat_id=chat_id,
            min_price=int(filters.min_price),
            max_price=int(filters.max_price),
            min_square=int(filters.min_square),
            max_square=int(filters.max_square),
            rooms_count=filters.rooms_type,
        )
            
    