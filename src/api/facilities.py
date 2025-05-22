import json
from fastapi import APIRouter

from src.api.dependensies import DB_Dep
from src.shemas.facilities import FacilitiesAdd
from src.init import redis_manager

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
async def get_all_servises(
    db: DB_Dep
):
    servises_from_cache = await redis_manager.get("servises")
    print(f"{servises_from_cache}")
    if not servises_from_cache:
        servises = await db.servises.get_all()
        servise_shemas: list[dict] = [data.model_dump() for data in servises]
        servise_json = json.dumps(servise_shemas)
        await redis_manager.set("servises", servise_json, 10)
        return servises
        
    servise_dicts = json.loads(servises_from_cache)    
    return servise_dicts