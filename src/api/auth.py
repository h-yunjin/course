from fastapi import APIRouter, HTTPException, Response
import sqlalchemy


from src.services.auth import AuthServise
from src.exeptions import ObjectAlreadyExistsExeption
from src.shemas.users import UserAdd, UserRequestAdd
from src.api.dependensies import DB_Dep, UserIdDEp


router = APIRouter(prefix="/auth", tags=["авторизация и аутонфикция"])


@router.get(
    "/me", summary="гет ми", description="тут можно узнать под чьим логином ты вошёл"
)
async def get_me(
    user_id: UserIdDEp,
    db: DB_Dep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return {"data": user}


@router.post("/register", summary="регистрация")
async def register(
    db: DB_Dep,
    data: UserRequestAdd,
):
    hashed_password = AuthServise().hashed_psw(data.password)
    hashed_data = UserAdd(email=data.email, password=hashed_password)
    try:
        await db.users.add(hashed_data)
        await db.commit()
    except ObjectAlreadyExistsExeption as ex:
        return HTTPException(status_code=409, detail="пользователь с таким имейлом уже зарегестрирован.")
    return {"status": "OK"}


@router.post("/login", summary="авторизация")
async def login(db: DB_Dep, data: UserRequestAdd, response: Response):
    user = await db.users.get_hashed_psw(email=data.email)
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
