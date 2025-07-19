# main.py

import httpx
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
import math

app = FastAPI(title="Star Wars API", description="An API to explore Star Wars characters and planets")
SWAPI_BASE_URL = "https://swapi.dev/api"
PAGE_SIZE = 10

async def _fetch_all_from_swapi(resource: str, search: Optional[str]):
    all_results = []
    url = f"{SWAPI_BASE_URL}/{resource}/"
    params = {"search": search} if search else None

    async with httpx.AsyncClient(verify=False) as client:
        first = True
        while url:
            try:
                if first:
                    response = await client.get(url, params=params)
                    first = False
                else:
                    response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                all_results.extend(data.get("results", []))
                url = data.get("next")
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error fetching {resource}: {str(e)}"
                )
    return all_results

def _sort_data(data: list, sort_by: str):
    data.sort(key=lambda item: str(item.get(sort_by, "")))
    return data

def _paginate_data(data: list, page: int, base_url: str):
    total_items = len(data)
    start_index = (page -1) * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    paginated_results = data[start_index:end_index]

    next_page_url = f"{base_url}?page={page + 1}" if end_index < total_items else None
    prev_page_url = f"{base_url}?page={page - 1}" if start_index > 0 else None

    return {
        "count": total_items,
        "next": next_page_url,
        "previous": prev_page_url,
        "results": paginated_results
    }

@app.get("/")
def read_root():
    return {"message": "Hello from the Star Wars API!"}

@app.get("/planets")
@app.get("/people")
async def get_resource(request: Request, page: int = 1, search: Optional[str] = None, sort_by: Optional[str] = None):
    resource = "people" if "people" in request.url.path else "planets"
    all_data = await _fetch_all_from_swapi(resource, search)
    if sort_by:
        all_data = _sort_data(all_data, sort_by)
    base_url = f"/{resource}?search={search or ''}&sort_by={sort_by or ''}"
    return _paginate_data(all_data, page, base_url)
    