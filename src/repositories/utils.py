from sqlalchemy import select, func
from datetime import date

from src.db import engine
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm



def get_id_bookings(
        date_from: date,
        date_to: date,
        hotel_id: int | None = None,
):
        rooms_count = (
            select(BookingsOrm.room_id, func.count("*")
            .label("rooms_booked"))
            .select_from(BookingsOrm)
            .filter(BookingsOrm.date_from <= date_to, BookingsOrm.date_to >= date_from)
            .group_by(BookingsOrm.room_id)
            .cte(name="rooms_count")
)
       

        rooms_left_table = (
            select(
                RoomsOrm.id.label("room_id"), 
                (RoomsOrm.quentity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left")
            )
            .select_from(RoomsOrm)    
            .outerjoin(rooms_count, RoomsOrm.id==rooms_count.c.room_id)
)
        
        if hotel_id is not None:
            rooms_left_table = rooms_left_table.filter(hotel_id==hotel_id)

        rooms_left_table = rooms_left_table.cte(name="rooms_left_table")    

        query = (
            select(rooms_left_table.c.room_id)
            .select_from(rooms_left_table)
            .filter(
                rooms_left_table.c.rooms_left>0,
                rooms_left_table.c.room_id.in_(select(RoomsOrm.id).select_from(RoomsOrm)
            )
))
     
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        return query