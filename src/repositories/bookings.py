from src.repositories.mappers.mappers import BookingsMapper
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepositories


class BookingsRepositories(BaseRepositories):
    model = BookingsOrm
    mapper = BookingsMapper