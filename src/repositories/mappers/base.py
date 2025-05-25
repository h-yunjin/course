from typing import TypeVar
from pydantic import BaseModel

from src.db import Base

DBModelType = TypeVar("DBModelType", bound=BaseModel)
ShemaType = TypeVar("ShemaType", bound=Base)


class Mapper:
    db_model: type[DBModelType] = None
    shema: type[ShemaType] = None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.shema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistance_entity(cls, data):
        return cls.db_model(**data.model_dump())
