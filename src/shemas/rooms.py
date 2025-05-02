from pydantic import BaseModel, Field



class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: float
    quentity: int


class PatchRoomAdd(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: float | None = Field(None)
    quentity: int | None = Field(None)


class Room(RoomAdd):
    id: int
    hotel_id: int
    title: str
    description: str
    price: float
    quentity: int    