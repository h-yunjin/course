# print(query.compile(engine, compile_kwargs={"literal_binds": True}))
from sqlalchemy import select, insert, delete, update
from src.db import engine
from pydantic import BaseModel


class BaseRepositories:
    model = None

    def __init__(self, session):
        self.session = session


    async def get_all(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query) 
        return result.scalars().all()
    

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
    
    

    async def add(self, data: BaseModel):
        add_data_stm = insert(self.model).values(data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stm)  
        return result.scalars().one()
    

    async def edit(self, data: BaseModel, exclude_unset: bool=False, **filter_by) -> None:
        edit_data_stm = update(self.model).filter_by(**filter_by).values(data.model_dump(exclude_unset=exclude_unset)) 
        print(edit_data_stm.compile(engine, compile_kwargs={"literal_binds": True})) 
        await self.session.execute(edit_data_stm)  


    async def delete(self, **filter_by):
        delete_data_stm = delete(self.model).filter_by(**filter_by).returning(self.model)  
        result = await self.session.execute(delete_data_stm)  
        return result.scalars().one()
         
