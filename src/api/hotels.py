from typing import Annotated
from fastapi import Query, Path, APIRouter, Body, Depends

from src.shemas.hotels import HotelAdd, PatchHotel
from src.api.dependensies import PaginationDep
from src.db import async_session_maker, engine
from src.repositories.hotels import HotelsRepositories



router = APIRouter(prefix="/hotels", tags=["отели"])




@router.get("",summary="получение данных")
async def get_hotels(pagination: PaginationDep,
               title: str | None = Query(None), 
               location: str | None = Query(None),
               ):
    per_page = pagination.per_page or 100
    async with async_session_maker() as session:
        return await HotelsRepositories(session).get_all(title, 
                                                        location, 
                                                        limit = per_page, 
                                                        ofset = per_page * (pagination.page - 1))



@router.post("",summary="добавление данных")
async def add_hotel(hotel_table: HotelAdd = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель 5 звезд у моря",
            "location": "Сочи. ул. Марата 24"
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель у фонтана",
            "location": "Дубай. ул. Суворовский 24"
        }
    }
})):
    
    async with async_session_maker() as session:
        hotels = await HotelsRepositories(session).add(hotel_table)
        await session.commit() 
        return {"status": "OK", "data": hotels}



@router.delete("/{hotel_id}",summary="удаление данных")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session: 
        hotel = await HotelsRepositories(session).delete(id=hotel_id)
        await session.commit()
        return {"status": "OK", "data": hotel}      



@router.put("/{hotel_id}",summary="обновление данных")
async def update_all(hotel_table: Annotated[HotelAdd, Depends()], hotel_id: int = Path(description="айдишник")):
    async with async_session_maker() as session:
        await HotelsRepositories(session).edit(hotel_table, id = hotel_id)
        await session.commit()
        return {"status": "OK"}



@router.patch("/{hotel_id}", summary="частичное обновление данных")
async def update(hotel_table: Annotated[PatchHotel, Depends()], hotel_id: int = Path(description="айдишник")):        
    async with async_session_maker() as session:
        await HotelsRepositories(session).edit(hotel_table, exclude_unset = True, id = hotel_id)
        await session.commit()
        return {"status": "OK"}    
    


@router.get("/{hotel_id}", summary="получение данных по айдишнику")
async def get_hotel(hotel_id: int = Path(description="айдишник")):
    async with async_session_maker() as session:
        return await HotelsRepositories(session).get_one_or_none(id=hotel_id)


    





