from src.models.bookings import BookingsOrm
from src.shemas.bookings import Bookings
from src.repositories.base import BaseRepositories


class BookingsRepositories(BaseRepositories):
    model = BookingsOrm
    shema = Bookings