from typing import Annotated
from fastapi import HTTPException, Query, Path, APIRouter, Body, Depends
from datetime import date
from fastapi_cache.decorator import cache

from src.exeptions import HotelNotFoundHTTPExeption, ObjectNotFoundExeption, check_date_to_date_from
from src.shemas.hotels import HotelAdd, PatchHotel
from src.api.dependensies import DB_Dep, PaginationDep
from src.tasks.tasks import sleepp


router = APIRouter(prefix="/hotels", tags=["отели"])


@router.get("", summary="получение всех отелей")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DB_Dep,
    title: str | None = Query(None),
    location: str | None = Query(None),
    date_from: date = Query(example="2025-05-06"),
    date_to: date = Query(example="2025-05-07"),
):
    per_page = pagination.per_page or 100
    check_date_to_date_from(date_to, date_from)
    hotels = await db.hotels.get_filtered_by_time(
        date_from,
        date_to,
        title,
        location,
        limit=per_page,
        ofset=per_page * (pagination.page - 1),
    )
    return {"data": hotels}


@router.post("", summary="добавление отеля")
async def add_hotel(
    db: DB_Dep,
    hotel_table: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель 5 звезд у моря",
                    "location": "Сочи. ул. Марата 24",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель у фонтана",
                    "location": "Дубай. ул. Суворовский 24",
                },
            },
        }
    ),
):
    hotels = await db.hotels.add(hotel_table)
    await db.commit()
    sleepp.delay()
    return {"status": "OK", "data": hotels}


@router.delete("/{hotel_id}", summary="удаление отеля")
async def delete_hotel(
    hotel_id: int,
    db: DB_Dep,
):
    hotel = db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="обновление отеля")
async def update_all(
    db: DB_Dep,
    hotel_table: Annotated[HotelAdd, Depends()],
    hotel_id: int = Path(description="айдишник"),
):
    await db.hotels.edit(hotel_table, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="частичное обновление отеля")
async def update(
    db: DB_Dep,
    hotel_table: Annotated[PatchHotel, Depends()],
    hotel_id: int = Path(description="айдишник"),
):
    await db.hotels.edit(hotel_table, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.get("/{hotel_id}", summary="получение отеля по айдишнику")
async def get_hotel(db: DB_Dep, hotel_id: int = Path(description="айдишник")):
    try:
        return await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundExeption as ex: 
        raise HotelNotFoundHTTPExeption

