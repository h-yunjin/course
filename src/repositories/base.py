from sqlalchemy import select, insert
from src.db import engine
from pydantic import BaseModel


class BaseRepositories:
    model = None
    def __init__(self, session):
        self.session = session

    async def get_all(self):
        query = select(self.model)
        # print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query) 
        return result.scalars().all()
    
    async def get_one_or_none(self, **filter):
        query = select(self.model).filter_by(**filter)
        result = await self.session.execute(query) 
        return result.scalars().one_or_none()
    
    async def add(self, data: BaseModel):
        add_hotel_stm = insert(self.model).values(data.model_dump()).returning(self.model)
        hotels = await self.session.execute(add_hotel_stm)  
        return hotels.scalars().one()
         
