from pydantic import BaseModel, Field

class FacilitiesAdd(BaseModel):
    title: str = Field()

class Facilities(FacilitiesAdd):
    id: int


class FacilitiesRoomAdd(BaseModel):
    room_id: int
    servise_id: int

class FacilitiesRoom(FacilitiesRoomAdd):
    id: int
