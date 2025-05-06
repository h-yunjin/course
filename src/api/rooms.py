from typing import Annotated
from fastapi import APIRouter, Body, Path, Depends

from src.api.dependensies import DB_Dep
from src.repositories.rooms import RoomsRepositories
from src.shemas.rooms import PatchRequestRoomAdd, PatchRoomAdd, RoomAdd, RoomRequestAdd
from src.db import async_session_maker

router = APIRouter(prefix="/hotels", tags=["номера"])



@router.get("/{hotel_id}/rooms/{room_id}", summary="получение данных определённого номера")
async def get_room(
    db: DB_Dep,
    hotel_id: int = Path(description="айдишник отеля"), 
    room_id: int = Path(description="айдишник номера")
):
    rooms = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    return {"data": rooms}    



@router.get("/{hotel_id}/rooms", summary="получение всех данных")
async def get_room(
    db: DB_Dep,
    hotel_id: int = Path(description="айдишник отеля")
):

    rooms = await db.rooms.get_filtered(hotel_id=hotel_id)
    return {"data": rooms}    



@router.post("/{hotel_id}/rooms", summary="добавление данных")
async def add_room(
    db: DB_Dep,
    hotel_id: int = Path(description="айдишник отеля"), 
    room_table: RoomRequestAdd = Body(openapi_examples={
    "1": {
        "summary": "1-ый номер",
        "value": {
            "title": "2 местный номер ",
            "description": "хороший",
            "price": "5.65",
            "quentity": "3"
        }
    },
    "2": {
        "summary": "2-ой номер",
        "value": {
            "title": "3 местный номер",
            "description": "неплохой",
            "price": "7.90",
            "quentity": "5"
        }
    }
})):
    _room_table = RoomAdd(hotel_id=hotel_id, **room_table.model_dump())
    rooms = await db.rooms.add(_room_table)
    await db.rooms.commit()
    return {"data": rooms}



@router.delete("/{hotel_id}/rooms", summary="удаление данных")
async def delete_room(
    db: DB_Dep,
    hotel_id: int = Path(description="айдишник отеля"), 
    room_id: int = Path(description="айдишник номера")
):
    room = db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.rooms.commit()
    return {"data": room}  



@router.put("/{hotel_id}/rooms/{room_id}", summary="обновление данных")
async def update_all(
    db: DB_Dep,
    room_table: RoomRequestAdd,
    hotel_id: int = Path(description="айдишник отеля"),
    room_id: int = Path(description="айдишник номера"),
):
    _room_table = RoomAdd(hotel_id=hotel_id, **room_table.model_dump())
    await db.rooms.edit(_room_table, id=room_id)
    await db.rooms.commit()
    return {"status": "OK"}    



@router.patch("/{hotel_id}/rooms/{room_id}", summary="частичное обновление данных")
async def update(
    db: DB_Dep,
    room_table: PatchRequestRoomAdd,
    hotel_id: int = Path( description="айдишник отеля"),
    room_id: int = Path(description="айдишник номера")
):
    _room_table = PatchRoomAdd(hotel_id=hotel_id, **room_table.model_dump(), exclude_unset=True)
    await db.rooms.edit(_room_table, id=room_id, hotel_id=hotel_id)
    await db.rooms.commit()
    return {"status": "OK"}    






  
