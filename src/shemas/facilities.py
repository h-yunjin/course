from pydantic import BaseModel, Field

class FacilitiesAdd(BaseModel):
    title: str = Field()

class Facilities(BaseModel):
    id: int
    title: str

