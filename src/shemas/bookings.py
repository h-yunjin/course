from pydantic import BaseModel
from datetime import date


class BookingsRequestAdd(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingsAdd(BookingsRequestAdd):
    user_id: int
    price: int


class Bookings(BookingsAdd):
    id: int
