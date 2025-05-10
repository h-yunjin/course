from src.db import engine
from src.shemas.rooms import Room
from src.repositories.base import BaseRepositories
from src.models.rooms import RoomsOrm
from src.repositories.utils import get_id_bookings

class RoomsRepositories(BaseRepositories):
    model = RoomsOrm
    shema = Room
    async def get_filtered_by_time(
            self, 
            date_from, 
            date_to, 
            hotel_id 
):
        rooms_ids_to_get = get_id_bookings(date_from, date_to, hotel_id)
        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))