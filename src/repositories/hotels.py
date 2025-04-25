from src.repositories.base import BaseRepositories
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func

class HotelsRepositories(BaseRepositories):
    model = HotelsOrm
    async def get_all(self, title, location, limit, ofset):
        query = select(self.model)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).like(f"%{location.lower()}%"))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).like(f"%{title.lower()}%"))

        query = (query
                .limit(limit)
                .offset(ofset)
                ) 
        # print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query) 
        return result.scalars().all()
    