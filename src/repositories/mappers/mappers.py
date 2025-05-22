from src.models.facilities import FacilitiesOrm, FacilitiesRoomsOrm
from src.shemas.facilities import Facilities, FacilitiesRoom
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.shemas.bookings import Bookings
from src.shemas.users import User
from src.shemas.rooms import Room
from src.models.hotels import HotelsOrm
from src.shemas.hotels import Hotel
from src.repositories.mappers.base import Mapper


class HotelMapper(Mapper):
    db_model = HotelsOrm
    shema = Hotel

class RoomMapper(Mapper):
    db_model = RoomsOrm
    shema = Room

class BookingsMapper(Mapper):
    db_model = BookingsOrm
    shema = Bookings

class UserMapper(Mapper):
    db_model = UsersOrm
    shema = User       

class ServiseMapper(Mapper):
    db_model = FacilitiesOrm
    shema = Facilities  

class ServiseRoomMapper(Mapper):
    db_model = FacilitiesRoomsOrm
    shema = FacilitiesRoom         