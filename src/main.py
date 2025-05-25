# ruff: noqa: F403
# ruff: noqa: E402
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn 


import sys
from pathlib import Path


from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


sys.path.append(str(Path(__file__).parent.parent))


from src.init import redis_manager
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.hotels import router as router_hotels
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images


@asynccontextmanager
async def lifespan(app: FastAPI):
   #при входе в систему
   await redis_manager.connect()
   FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
   yield
   #при выходе из системы
   await redis_manager.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)



from src.db import *  

if __name__ == "__main__":
       uvicorn.run("main:app", reload=True)



