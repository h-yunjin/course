from fastapi import Query, Path, APIRouter
from shemas.hotels import Hotel, PatchHotel

from src.api.dependensies import PaginationDep





router = APIRouter(prefix="/hotels", tags=["отели"])



hotels = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Санкт-Петербуог", "name": "sankt-petesburg"},
    {"id": 4, "title": "Москва", "name": "moskow"},
    {"id": 5, "title": "Стерлитамак", "name": "sterlitamak"},
    {"id": 6, "title": "Уфа", "name": "ufa"},
    {"id": 7, "title": "Киров", "name": "kirov"},
    {"id": 8, "title": "Донецк", "name": "donezck"},
]    

@router.get("",
            summary="получение данных")
def get_hotels(pagination: PaginationDep,
               title: str | None = Query(None, description="город"), 
               id: int | None = Query(None, description="айдишник"),
               ):
        hotels_ = []
        for hotel in hotels:
            if id and id != hotel["id"]:
                    continue
            if title and title != hotel["title"]:
                    continue
            hotels_.append(hotel)
        if pagination.page and pagination.per_page:
            return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
        if pagination.page and not pagination.per_page:
            return hotels_[4 * (pagination.page - 1):][:4]
        if not pagination.page and pagination.per_page:
            return hotels_[:pagination.per_page]
        return hotels_

@router.delete("/{hotel_id}",
            summary="удаление данных")
def delete_hotel(hotel_id: int = Path(description="айдишник")):
    global hotels
    holels = [hotel for hotel in hotels if hotel["id"] != hotel_id]  
    return {"status": "OK"}      

@router.post("",
            summary="добавление данных")
def add_hotel(hotel_table: Hotel):
    global hotels
    hotels.append(
           {
                "id": hotels[-1]["id"] + 1,
                "title": hotel_table.title,
                "name": hotel_table.name,
           }
    )
    return {"status": "OK"}

@router.put("/{hotel_id}",
            summary="обновление данных")
def update_all(hotel_table: Hotel, hotel_id: int = Path(description="айдишник")):
    for hotel in hotels:
        if hotel_id == hotel["id"]:
            hotel["title"] = hotel_table.title
            hotel["name"] = hotel_table.name
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
        
