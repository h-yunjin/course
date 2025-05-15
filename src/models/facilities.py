from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

class FacilitiesOrm(Base):
    __tablename__ = "servises"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))

    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="servises",
        secondary="servises_rooms",
    )


class FacilitiesRoomsOrm(Base):
    __tablename__ = "servises_rooms"   

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    servise_id: Mapped[int] = mapped_column(ForeignKey("servises.id"))


    
