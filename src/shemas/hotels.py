from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str
    location: str

class PatchHotel(BaseModel):
    title: str | None = Field(None, description="город"), 
    location: str | None = Field(None, description="имя")     




