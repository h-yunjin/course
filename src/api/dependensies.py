from typing import Annotated
from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel

from src.services.auth import AuthServise
from src.db import async_session_maker
from src.utils.db_manager import DB_Manager

class Pagination(BaseModel):
    page: Annotated[int | None, Query(1, gt=0)]
    per_page: Annotated[int | None, Query(None, gt=0, lt=30)]

PaginationDep = Annotated[Pagination, Depends()]    

def get_token(request: Request):
    token = request.cookies.get("access_token", None)
    if token is None:
        raise HTTPException(status_code=401, detail="нет токена доступа. дурак")
    return token


def current_user_id(token: Annotated[str, Depends(get_token)]) -> int:
    data = AuthServise().decode_token(token)
    return data["user_id"]


UserIdDEp = Annotated[str, Depends(current_user_id)]


async def get_db():
    async with DB_Manager(async_session_maker) as db:
        yield db


DB_Dep = Annotated[DB_Manager, Depends(get_db)]