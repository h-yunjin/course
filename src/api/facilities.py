from fastapi import APIRouter

from src.api.dependensies import DB_Dep
from src.shemas.facilities import FacilitiesAdd

router = APIRouter(prefix="/servises", tags=["удобства"])


@router.post("", summary="получение всех удобств")
async def add_servises(
    db: DB_Dep,
    title: FacilitiesAdd
):
    servise = await db.servises.add(title)
    await db.commit()
    return {"data": servise}


@router.get("", summary="добавление удобств")
async def get_all_servises(
    db: DB_Dep
):
    servises = await db.servises.get_all()
    return {"data": servises}