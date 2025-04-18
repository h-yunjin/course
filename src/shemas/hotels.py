from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str
    name: str

class PatchHotel(BaseModel):
    title: str | None = Field(None, description="город"), 
    name: str | None = Field(None, description="имя")     
