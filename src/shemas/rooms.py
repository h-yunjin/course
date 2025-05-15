from pydantic import BaseModel, Field

from src.shemas.facilities import Facilities

class RoomRequestAdd(BaseModel):
    title: str
    description: str | None = Field(None)
    price: float
    quentity: int
    servises_ids: list[int] | None = []


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = Field(None)
    price: float
    quentity: int


class PatchRequestRoomAdd(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: float | None = Field(None)
    quentity: int | None = Field(None)  
    servises_ids: list[int] | None = None


class PatchRoomAdd(BaseModel):
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: float | None = Field(None)
    quentity: int | None = Field(None)


class Room(RoomAdd):
    id: int

class RoomWithRels(Room):
    servises: list[Facilities]    