from typing import Annotated
from fastapi import APIRouter, Body, Path, Depends


from src.repositories.rooms import RoomsRepositories
from src.shemas.rooms import PatchRoomAdd, RoomAdd
from src.db import async_session_maker

router = APIRouter(prefix="/hotels", tags=["номера"])

@router.get("/{hotel_id}/room", summary="получение данных")
async def get_room(hotel_id: int = Path(description="айдишник отеля")):
    async with async_session_maker() as session:
        rooms = await RoomsRepositories(session).get_all(hotel_id=hotel_id)
    return {"data": rooms}    



@router.post("/room", summary="добавление данных")
async def add_room(room_table: RoomAdd = Body(openapi_examples={
    "1": {
        "summary": "1-ый номер",
        "value": {
            "hotel_id": "37",
            "title": "2 местный номер ",
            "description": "хороший",
            "price": "5.65",
            "quentity": "3"
        }
    },
    "2": {
        "summary": "2-ой номер",
        "value": {
            "hotel_id": "38",
            "title": "3 местный номер",
            "description": "неплохой",
            "price": "7.90",
            "quentity": "5"
        }
    }
})):
    async with async_session_maker() as session:
        rooms = await RoomsRepositories(session).add(room_table)
        await session.commit()
    return {"data": rooms}



@router.delete("/{room_id}/room", summary="удаление данных")
async def delete_room(room_id: int = Path(description="айдишник номера")):
    async with async_session_maker() as session:
        room = await RoomsRepositories(session).delete(id=room_id)
        await session.commit()
    return {"data": room}  



@router.put("/{room_id}/room", summary="обновление данных")
async def update_all(
    room_table: Annotated[RoomAdd, Depends()],
    room_id: int = Path(description="айдишник номера"),
):
    async with async_session_maker() as session:
        await RoomsRepositories(session).edit(room_table, id=room_id)
        await session.commit()
    return {"status": "OK"}    



@router.patch("/{room_id}/room", summary="частичное обновление данных")
async def update(
    room_table: Annotated[PatchRoomAdd, Depends()],
    room_id: int = Path(description="айдишник номера")
):
    async with async_session_maker() as session:
        await RoomsRepositories(session).edit(room_table, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "OK"}    






  
