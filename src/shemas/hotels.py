from pydantic import BaseModel, Field

class HotelAdd(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None) 


class Hotel(HotelAdd):
    id: int 


class PatchHotel(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)   






