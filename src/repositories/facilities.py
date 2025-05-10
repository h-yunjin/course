from src.models.facilities import FacilitiesOrm
from src.repositories.base import BaseRepositories
from src.shemas.facilities import Facilities


class FacilitiesRepositories(BaseRepositories):
    model=FacilitiesOrm
    shema=Facilities