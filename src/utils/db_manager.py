from src.repositories.facilities import (
    FacilitiesRepositories,
    FacilitiesRoomRepositories,
)
from src.repositories.bookings import BookingsRepositories
from src.repositories.hotels import HotelsRepositories
from src.repositories.rooms import RoomsRepositories
from src.repositories.users import UsersRepositories


class DB_Manager:
    def __init__(self, async_session_maker):
        self.async_session_maker = async_session_maker

    async def __aenter__(self):
        self.session = self.async_session_maker()

        self.hotels = HotelsRepositories(self.session)
        self.rooms = RoomsRepositories(self.session)
        self.users = UsersRepositories(self.session)
        self.bookings = BookingsRepositories(self.session)
        self.servises = FacilitiesRepositories(self.session)
        self.servisesroom = FacilitiesRoomRepositories(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
