from fastapi import APIRouter

from src.api.dependensies import DB_Dep, UserIdDEp
from src.shemas.bookings import BookingsAdd, BookingsRequestAdd

router = APIRouter(prefix="/bookings", tags=["бронирование"])



@router.post("", summary="бронирование")
async def booking(
    book_table: BookingsRequestAdd,
    db: DB_Dep,
    user_id: UserIdDEp,
):
    room = await db.rooms.get_one_or_none(id=book_table.room_id)
    _book_table = BookingsAdd(user_id=user_id, **book_table.model_dump(), price=room.price)
    booking = await db.bookings.add(_book_table)
    await db.commit()
    return {"data": booking}


@router.get("", summary="получение всех бронирований")
async def get_all_bookings(
    db: DB_Dep
):
    bookings = await db.bookings.get_all()
    return {"data": bookings}


@router.get("/me", summary="получение бронирований этого аккаунта")
async def get_my_bookings(
    db: DB_Dep,
    user_id: UserIdDEp
):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return {"data": bookings}