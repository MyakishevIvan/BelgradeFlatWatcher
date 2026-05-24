from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from data_base.models.base import Base
from pages.components.flat_components.flat import Flat


class SeenFlat(Base):
    __tablename__ = "seen_flats"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_user_id: Mapped[int] = mapped_column(Integer)
    flat_url: Mapped[str] = mapped_column(String)
    flat_id: Mapped[int] = mapped_column(Integer)

    def __eq__(self, other):
        if not isinstance(other, SeenFlat):
            return False
        return (
                self.telegram_user_id == other.telegram_user_id
                and self.flat_url == other.flat_url
                and self.flat_id == other.flat_id
        )

    @classmethod
    def from_flat(
            cls,
            telegram_user_id: int,
            flat: Flat,
    ) -> "SeenFlat":
        return cls(
            telegram_user_id=telegram_user_id,
            flat_url=flat.url,
            flat_id=flat.id,
        )