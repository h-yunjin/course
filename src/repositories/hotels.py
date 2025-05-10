from src.models.rooms import RoomsOrm
from src.repositories.utils import get_id_bookings
from shemas.hotels import Hotel
from src.repositories.base import BaseRepositories
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func

from src.db import engine

class HotelsRepositories(BaseRepositories):
    model = HotelsOrm
    shema = Hotel
    
    async def get_filtered_by_time(
            self,
            date_from, 
            date_to, 
            title, 
            location, 
            limit, 
            ofset
):
        rooms_ids_to_get = get_id_bookings(date_from, date_to)
        query = (
            select(RoomsOrm.hotel_id)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        if location:
            query = query.filter(func.lower(HotelsOrm.location).like(f"%{location.lower()}%"))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).like(f"%{title.lower()}%"))
        query = query.limit(limit).offset(ofset)
        return await self.get_filtered(HotelsOrm.id.in_(query))
       