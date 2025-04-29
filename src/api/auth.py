from fastapi import APIRouter
from passlib.context import CryptContext

from src.db import async_session_maker
from src.repositories.users import UsersRepositories
from src.shemas.users import UserAdd, UserRequestAdd

router = APIRouter(prefix="/auth", tags=["авторизация и аутонфикция"])



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)
    hashed_data = UserAdd(email=data.email, password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepositories(session).add(hashed_data)
        await session.commit()
    return {"status": "OK"}    