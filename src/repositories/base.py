# print(query.compile(engine, compile_kwargs={"literal_binds": True}))
from sqlalchemy import exists, select, insert, delete, update
from pydantic import BaseModel
import sqlalchemy
from asyncpg.exceptions import UniqueViolationError

from src.exeptions import  ObjectAlreadyExistsExeption, ObjectNotFoundExeption
from src.repositories.mappers.base import Mapper
from src.db import engine


class BaseRepositories:
    model = None
    mapper: Mapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter_by(**filter_by).filter(*filter)
        result = await self.session.execute(query)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        return [
            self.mapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_all(self):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)
    
    
    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except sqlalchemy.exc.NoResultFound:
            raise ObjectNotFoundExeption
        return self.mapper.map_to_domain_entity(model)


    async def add(self, data: BaseModel):
        try:
            add_data_stm = (
                insert(self.model).values(**data.model_dump()).returning(self.model)
            )
            result = await self.session.execute(add_data_stm)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except sqlalchemy.exc.IntegrityError as ex:
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsExeption from ex          
            else: 
                raise ex


    async def add_bulk(self, data: list[BaseModel]) -> None:
        add_data_stm = insert(self.model).values([item.model_dump() for item in data])
        return await self.session.execute(add_data_stm)


    async def edit(
        self, data: BaseModel, exclude_unset: bool = False, **filter_by
    ) -> None:
        edit_data_stm = (
            update(self.model)
            .filter_by(**filter_by)
            .values(data.model_dump(exclude_unset=exclude_unset))
        )
        return await self.session.execute(edit_data_stm)
        


    async def delete(self, **filter_by) -> BaseModel:
        delete_data_stm = (
            delete(self.model).filter_by(**filter_by).returning(self.model)
        )
        result = await self.session.execute(delete_data_stm)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)
