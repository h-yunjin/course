from fastapi import FastAPI
import uvicorn 


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))


from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.hotels import router as router_hotels



app = FastAPI()

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)


from src.db import *  

if __name__ == "__main__":
       uvicorn.run("main:app", reload=True)



