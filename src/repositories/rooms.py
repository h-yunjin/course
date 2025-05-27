from sqlalchemy import select
from sqlalchemy.orm import joinedload


from src.repositories.mappers.mappers import RoomMapper
from src.db import engine
from src.shemas.rooms import RoomWithRels
from src.repositories.base import BaseRepositories
from src.models.rooms import RoomsOrm
from src.repositories.utils import get_id_bookings


class RoomsRepositories(BaseRepositories):
    model = RoomsOrm
    mapper = RoomMapper

    async def get_filtered_by_time(self, date_from, date_to, hotel_id):
        rooms_ids_to_get = get_id_bookings(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(joinedload(self.model.servises))
            .filter(self.model.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        return [
            RoomWithRels.model_validate(model, from_attributes=True)
            for model in result.unique().scalars().all()
        ]

    async def get_one_or_none_with_rels(self, id, hotel_id):
        query = (
            select(self.model)
            .options(joinedload(self.model.servises))
            .filter_by(id=id, hotel_id=hotel_id)
        )
        result = await self.session.execute(query)
        model_ = result.unique().scalars().all()
        return [
            RoomWithRels.model_validate(model, from_attributes=True)
            for model in model_
        ]



       
