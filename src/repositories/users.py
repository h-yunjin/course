from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import UsersOrm
from src.repositories.mappers.mappers import UserMapper
from src.shemas.users import UserHashedPsw
from src.repositories.base import BaseRepositories


class UsersRepositories(BaseRepositories):
    model=UsersOrm
    mapper = UserMapper

    async def get_hashed_psw(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        res = await self.session.execute(query)
        model = res.scalars().one()
        return UserHashedPsw.model_validate(model, from_attributes=True)
