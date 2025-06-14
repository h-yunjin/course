from datetime import date
from fastapi import APIRouter, Body, HTTPException, Path, Query

from src.exeptions import HotelNotFoundHTTPExeption,  ObjectNotFoundExeption, RoomNotFoundHTTPExeption, check_date_to_date_from
from src.shemas.facilities import FacilitiesRoomAdd
from src.api.dependensies import DB_Dep
from src.shemas.rooms import PatchRequestRoomAdd, PatchRoomAdd, RoomAdd, RoomRequestAdd


router = APIRouter(prefix="/hotels", tags=["номера"])


@router.get(
    "/{hotel_id}/rooms/{room_id}", summary="получение данных определённого номера"
)
async def get_room(
    db: DB_Dep,
    hotel_id: int = Path(description="айдишник отеля"),
    room_id: int = Path(description="айдишник номера"),
):
    room = await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)
    if not room:
        raise RoomNotFoundHTTPExeption
    return room


@router.get("/{hotel_id}/rooms", summary="получение всех номеров")
async def get_all_rooms(
    db: DB_Dep,
    date_from: date = Query(example="2025-05-06"),
    date_to: date = Query(example="2025-05-07"),
    hotel_id: int = Path(description="айдишник отеля"),
):
    check_date_to_date_from(date_to, date_from)
    rooms = await db.rooms.get_filtered_by_time(
        date_from=date_from, date_to=date_to, hotel_id=hotel_id
        )
    return {"data": rooms}
    
        


@router.post("/{hotel_id}/rooms", summary="добавление номера")
async def add_room(
    db: DB_Dep,
    hotel_id: int = Path(description="айдишник отеля"),
    room_table: RoomRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "1-ый номер",
                "value": {
                    "title": "2 местный номер ",
                    "description": "хороший",
                    "price": "5.65",
                    "quentity": "3",
                    "servises_ids": [8, 9],
                },
            },
            "2": {
                "summary": "2-ой номер",
                "value": {
                    "title": "3 местный номер",
                    "description": "неплохой",
                    "price": "7.90",
                    "quentity": "5",
                    "servises_ids": [8, 9],
                },
            },
        }
    ),
):
    _room_table = RoomAdd(hotel_id=hotel_id, **room_table.model_dump())
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundExeption as ex:
        raise HotelNotFoundHTTPExeption
    rooms = await db.rooms.add(_room_table)
    rooms_servises = [
        FacilitiesRoomAdd(room_id=rooms.id, servise_id=sr_id)
        for sr_id in room_table.servises_ids
    ]
    await db.servisesroom.add_bulk(rooms_servises)
    await db.commit()
    return {"data": rooms}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="удаление номера")
async def delete_room(
    db: DB_Dep,
    hotel_id: int = Path(description="айдишник отеля"),
    room_id: int = Path(description="айдишник номера"),
):
    try:
        await db.rooms.get_one(id=hotel_id)
    except ObjectNotFoundExeption as ex:
        raise RoomNotFoundHTTPExeption
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundExeption as ex:
        raise HotelNotFoundHTTPExeption    
    room = await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="обновление номера")
async def update_all(
    db: DB_Dep,
    room_table: RoomRequestAdd,
    hotel_id: int = Path(description="айдишник отеля"),
    room_id: int = Path(description="айдишник номера"),
):
    _room_table = RoomAdd(hotel_id=hotel_id, **room_table.model_dump())
    try:
        await db.rooms.get_one(id=hotel_id)
    except ObjectNotFoundExeption as ex:
        raise RoomNotFoundHTTPExeption
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundExeption as ex:
        raise HotelNotFoundHTTPExeption    
    await db.rooms.edit(_room_table, id=room_id)
    await db.servisesroom.edit_servises(room_id, room_table.servises_ids)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="частичное обновление номера")
async def update(
    db: DB_Dep,
    room_table: PatchRequestRoomAdd,
    hotel_id: int = Path(description="айдишник отеля"),
    room_id: int = Path(description="айдишник номера"),
):
    _room_table = PatchRoomAdd(
        hotel_id=hotel_id, **room_table.model_dump(exclude_unset=True)
    )
    try:
        await db.rooms.get_one(id=hotel_id)
    except ObjectNotFoundExeption as ex:
        raise RoomNotFoundHTTPExeption
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundExeption as ex:
        raise HotelNotFoundHTTPExeption
    await db.rooms.edit(_room_table, exclude_unset=True, id=room_id, hotel_id=hotel_id)  
    if room_table.servises_ids is not None:
        await db.servisesroom.edit_servises(room_id, room_table.servises_ids)
    await db.commit()
    return {"status": "OK"}
