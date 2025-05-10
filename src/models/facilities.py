from sqlalchemy import ForeignKey, String
from src.db import Base
from sqlalchemy.orm import Mapped, mapped_column

class FacilitiesOrm(Base):
    __tablename__ = "servises"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))


class FacilitiesRoomsOrm(Base):
    __tablename__ = "servises_rooms"   

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    servise_id: Mapped[int] = mapped_column(ForeignKey("servises.id"))
