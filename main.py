from fastapi import FastAPI
import uvicorn 

from hotels import router as router_hotels

app = FastAPI()

app.include_router(router_hotels)

if 1 == 1:
    print(f"j")  

if __name__ == "__main__":
       uvicorn.run("main:app", reload=True)



