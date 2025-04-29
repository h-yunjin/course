from shemas.hotels import Hotel
from src.repositories.base import BaseRepositories
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func

class HotelsRepositories(BaseRepositories):
    model = HotelsOrm
    shema = Hotel
    async def get_all(self, title, location, limit, ofset):
        query = select(self.model)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).like(f"%{location.lower()}%"))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).like(f"%{title.lower()}%"))
        query = query.limit(limit).offset(ofset)
        result = await self.session.execute(query) 
        return [self.shema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
    