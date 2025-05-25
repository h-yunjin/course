from sqlalchemy import insert, select, delete

from src.repositories.mappers.mappers import ServiseMapper, ServiseRoomMapper
# from src.db import engine
from src.models.facilities import FacilitiesOrm, FacilitiesRoomsOrm
from src.repositories.base import BaseRepositories


class FacilitiesRepositories(BaseRepositories):
    model=FacilitiesOrm
    mapper = ServiseMapper

class FacilitiesRoomRepositories(BaseRepositories):
    model=FacilitiesRoomsOrm
    mapper = ServiseRoomMapper
 
    async def edit_servises(self, room_id: int, servises_ids: list[int]) -> None:
        query = (
            select(FacilitiesRoomsOrm.servise_id)
           .filter(FacilitiesRoomsOrm.room_id==room_id)
)
        res = await self.session.execute(query)
        following_ids = res.scalars().all()
        
        del_execute: list[int] = list(set(following_ids) - set(servises_ids))
        insert_execute: list[int] = list(set(servises_ids) - set(following_ids))

        if del_execute:
            del_query = (
                delete(FacilitiesRoomsOrm)
                .filter(FacilitiesRoomsOrm.room_id==room_id, FacilitiesRoomsOrm.servise_id.in_(del_execute))
)
            await self.session.execute(del_query)
            
        if insert_execute:
            insert_query = (
                insert(FacilitiesRoomsOrm)
                .values([{"room_id": room_id, "servise_id": sr_id} for sr_id in insert_execute])
            )   
            await self.session.execute(insert_query)



       