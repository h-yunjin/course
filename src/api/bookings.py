from fastapi import APIRouter, HTTPException

from src.shemas.rooms import Room
from src.exeptions import All_Rooms_Are_Booked_Exeption, ObjectNotFoundExeption, RoomNotFoundHTTPExeption
from src.api.dependensies import DB_Dep, UserIdDEp
from src.shemas.bookings import BookingsAdd, BookingsRequestAdd

router = APIRouter(prefix="/bookings", tags=["бронирование"])


@router.post("", summary="бронирование")
async def booking(
    book_table: BookingsRequestAdd,
    db: DB_Dep,
    user_id: UserIdDEp,
):
    try:
        room: Room = await db.rooms.get_one(id=book_table.room_id)
    except ObjectNotFoundExeption as ex:
        raise RoomNotFoundHTTPExeption
    _book_table = BookingsAdd(
        user_id=user_id, **book_table.model_dump(), price=room.price
    )
    try:
        booking = await db.bookings.add_bookings(_book_table, room.hotel_id)
    except All_Rooms_Are_Booked_Exeption as ex:
        raise HTTPException(status_code=409, detail=ex.detail)     
    await db.commit()
    return {"data": booking}


@router.get("", summary="получение всех бронирований")
async def get_all_bookings(db: DB_Dep):
    bookings = await db.bookings.get_all()
    return {"data": bookings}


@router.get("/me", summary="получение бронирований этого аккаунта")
async def get_my_bookings(db: DB_Dep, user_id: UserIdDEp):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return {"data": bookings}
