from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependensies import DB_Dep
from src.shemas.facilities import FacilitiesAdd

router = APIRouter(prefix="/servises", tags=["удобства"])


@router.post("", summary="добавление удобств")
async def add_servises(
    db: DB_Dep,
    title: FacilitiesAdd
):
    servise = await db.servises.add(title)
    await db.commit()
    return {"data": servise}


@router.get("", summary="получение всех удобств")
@cache(expire=60)
async def get_all_servises(
    db: DB_Dep
):
    print("ble")
    return await db.servises.get_all()
        