from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
import typing

if typing.TYPE_CHECKING:
    from src.models.facilities import FacilitiesOrm

from src.db import Base


class RoomsOrm(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None]
    price: Mapped[int]
    quentity: Mapped[int]

    servises: Mapped[list["FacilitiesOrm"]] = relationship(
        back_populates="rooms",
        secondary="servises_rooms",
    )
