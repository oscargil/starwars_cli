# main.py

import httpx
from typing import Optional
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Star Wars API", description="An API to explore Star Wars characters and planets")
SWAPI_BASE_URL = "https://swapi.dev/api"

@app.get("/")
def read_root():
    return {"message": "Welcome to the Star Wars API!"}

async def _fetch_from_swapi(resource: str, page: int, search: Optional[str]):
    params = {"page": page}
    if search:
        params["search"] = search
    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(f"{SWAPI_BASE_URL}/{resource}/", params=params)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error fetching {resource}: {str(e)}")

@app.get("/planets")
async def get_planets(page: int = 1, search: Optional[str] = None):
    return await _fetch_from_swapi("planets", page, search)
    

@app.get("/people")
async def get_people(page: int = 1, search: Optional[str] = None):
    return await _fetch_from_swapi("people", page, search)
    