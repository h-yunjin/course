

from datetime import date

from fastapi import HTTPException


class NabronirovalExeption(Exception):
    detail = "неожиданная ошибка"
    def __init__(self):
        super().__init__(self.detail)

class ObjectNotFoundExeption(NabronirovalExeption):
    detail = "объект не найден. дура"    

class All_Rooms_Are_Booked_Exeption(NabronirovalExeption):
    detail = "все комнтаты заняты. дура"      

class ObjectAlreadyExistsExeption(NabronirovalExeption):
    detail = "объект уже существует. дура"       


def check_date_to_date_from(date_to: date, date_from: date) -> bool:
    if date_from >= date_to:
        raise HTTPException(status_code=400, detail="дата заезда и выезда введены не правильно. дура")
    
class NabronirovalHTTPExeption(HTTPException):
    status_code = 500
    detail = None    
    def __init__(self):
        super().__init__(detail=self.detail, status_code=self.status_code)
         
class HotelNotFoundHTTPExeption(NabronirovalHTTPExeption):
    status_code = 404
    detail = "отель не найден. дура"    

class RoomNotFoundHTTPExeption(NabronirovalHTTPExeption):
    status_code = 404
    detail = "номер не найден. дура" 