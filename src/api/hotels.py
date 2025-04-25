from fastapi import Query, Path, APIRouter, Body
from sqlalchemy import insert, select, delete, func

from src.shemas.hotels import Hotel, PatchHotel
from src.api.dependensies import PaginationDep
from src.db import async_session_maker, engine
from src.models.hotels import HotelsOrm


router = APIRouter(prefix="/hotels", tags=["отели"])

from src.repositories.hotels import HotelsRepositories

@router.get("",
            summary="получение данных")
async def get_hotels(pagination: PaginationDep,
               title: str | None = Query(None, description="название отеля"), 
               location: str | None = Query(None, description="местоположение"),
               ):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepositories(session).get_all(title, 
                                                        location, 
                                                        limit = per_page, 
                                                        ofset = per_page * (pagination.page - 1))


    


@router.delete("/{hotel_id}",
            summary="удаление данных")
async def delete_hotel(hotel_id: int = Path(description="айдишник")):
    async with async_session_maker() as session:
        delete_src = delete(HotelsOrm).where(HotelsOrm.id == hotel_id)   
        await session.execute(delete_src)  
        await session.commit()
    return {"status": "OK"}      



@router.post("",
            summary="добавление данных")
async def add_hotel(hotel_table: Hotel = Body(openapi_examples={
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
        # await HotelsRepositories(session).add(hotel_table)
        hotels = await HotelsRepositories(session).add(hotel_table)
        await session.commit() 
        return {"status": "OK", "data": hotels}
        

@router.put("/{hotel_id}",
            summary="обновление данных")
async def update_all(hotel_table: Hotel, hotel_id: int = Path(description="айдишник")):
    async with async_session_maker() as session:
        add_hotel_stm = update({'no_of_logins': User.no_of_logins + 1})   
        await session.execute(add_hotel_stm)  
        await session.commit()
        return {"status": "OK"}



@router.patch("/{hotel_id}",
            summary="частичное обновление данных")
def update(hotel_table: PatchHotel, hotel_id: int = Path(description="айдишник")):
    for hotel in hotels:
        if hotel_id == hotel["id"]:
            if hotel_table.title:
                hotel["title"] = hotel_table.title
            if hotel_table.name:    
                hotel["name"] = hotel_table.name
            return {"status": "OK"}        
        
