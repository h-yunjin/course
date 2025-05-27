

from src.exeptions import All_Rooms_Are_Booked_Exeption
from src.shemas.bookings import BookingsAdd
from src.repositories.utils import get_id_bookings
from src.repositories.mappers.mappers import BookingsMapper
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepositories


class BookingsRepositories(BaseRepositories):
    model = BookingsOrm
    mapper = BookingsMapper

    async def add_bookings(self, data: BookingsAdd, hotel_id: int):
        free_rooms_ids = get_id_bookings(date_from=data.date_from, date_to=data.date_to, hotel_id=hotel_id)
        result = await self.session.execute(free_rooms_ids)
        model: list[int] = result.scalars().all()

        if data.room_id in model:
            return await self.add(data)
        raise All_Rooms_Are_Booked_Exeption


        
