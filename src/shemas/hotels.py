from pydantic import BaseModel, Field

class HotelAdd(BaseModel):
    title: str
    location: str

class Hotel(HotelAdd):
    id: int  

class PatchHotel(BaseModel):
    title: str | None = Field(None, description="город"), 
    location: str | None = Field(None, description="имя")     




