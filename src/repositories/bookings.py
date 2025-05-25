from datetime import date

from src.repositories.mappers.mappers import BookingsMapper
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepositories


class BookingsRepositories(BaseRepositories):
    model = BookingsOrm
    mapper = BookingsMapper


    async def get_bookings_with_today(self):
        today = date.today()
        self.get_filtered(date_from=today)
