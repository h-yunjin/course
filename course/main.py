from fastapi import FastAPI, Query, Body
import uvicorn 
from typing import Optional

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"}
]

@app.get("/hotels")
def get_hotels(title: str | None = Query(None, description="city"), 
               id: int | None = Query(None, description="id")):
        hotels_ = []
        for hotel in hotels:
                if id and id != hotel["id"]:
                        continue
                if title and title != hotel["title"]:
                        continue
                if not title and not id:
                       continue
                hotels_.append(hotel)
        return hotels_

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    holels = [hotel for hotel in hotels if hotel["id"] != hotel_id]  
    return {"status": "OK"}      

@app.post("/hotels")
def add_hotel(title: str = Body(embed=True)):
    global hotels
    hotels.append(
           {
                "id": hotels[-1]["id"] + 1,
                "title": title
           }
    )
    return {"status": "OK"}

@app.put("/hotels/{hotel_id}")
def update_al(hotel_id: int, title: str = Body(), name: str = Body()):
    for hotel in hotels:
        if hotel_id == hotel["id"]:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "OK"}
        

@app.patch("/hotels/{hotel_id}")
def update(hotel_id: int, 
               title: str | None = Body(None), 
               name: str | None = Body(None)):
    for hotel in hotels:
        if hotel_id == hotel["id"]:
            if title:
                hotel["title"] = title
            if name:    
                hotel["name"] = name
            return {"status": "OK"}        
        

if __name__ == "__main__":
       uvicorn.run("main:app", reload=True)

