from typing import Annotated
from fastapi import APIRouter, HTTPException, Response, Depends

import sqlalchemy


from src.services.auth import AuthServise
from src.db import async_session_maker
from src.repositories.users import UsersRepositories
from src.shemas.users import UserAdd, UserRequestAdd
from src.api.dependensies import UserIdDEp


router = APIRouter(prefix="/auth", tags=["авторизация и аутонфикция"])


@router.get("/me", summary="гет ми", description="тут можно узнать под чьим логином ты вошёл")
async def get_me(user_id: UserIdDEp):
   async with async_session_maker() as session:
       user = await UsersRepositories(session).get_one_or_none(id=user_id)
       return {"data": user}
   


@router.post("/register", summary="регистрация")
async def register(
    data: Annotated[UserRequestAdd, Depends()]
):
    hashed_password = AuthServise().hashed_psw(data.password)
    hashed_data = UserAdd(email=data.email, password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UsersRepositories(session).add(hashed_data)
        except sqlalchemy.exc.IntegrityError:
            return f"ты дурак. такой емейл уже существует"        
        await session.commit()
    return {"status": "OK"}
  


@router.post("/login", summary="авторизация")
async def login(
    data: Annotated[UserRequestAdd, Depends()], 
    response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepositories(session).get_hashed_psw(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="пользователя нет. дурак")
        if not AuthServise().verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail="Пароль неверный . дурак")
        access_token = AuthServise().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}



@router.post("/logout", summary="выйти")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
