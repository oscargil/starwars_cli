import httpx
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
import math
from fastapi.responses import JSONResponse
from backend.services.swapi_service import SwapiService
from backend.services.exceptions import SwapiError

app = FastAPI(title="Star Wars API", description="An API to explore Star Wars characters and planets")

swapi_service = SwapiService(httpx.AsyncClient(verify=False))

@app.get("/")
def read_root():
    """Root endpoint for health check or welcome message."""
    return {"message": "Hello from the Star Wars API!"}

@app.get("/planets")
@app.get("/people")
async def get_resource(request: Request, page: int = 1, search: Optional[str] = None, sort_by: Optional[str] = None):
    """Proxy endpoint for people and planets with pagination, search, and sorting."""
    resource = "people" if "people" in request.url.path else "planets"
    all_data = await swapi_service.fetch_all(resource, search)
    all_data = swapi_service.sort_data(all_data, sort_by)
    base_url = f"/{resource}?search={search or ''}&sort_by={sort_by or ''}"
    return swapi_service.paginate(all_data, page, base_url)

@app.exception_handler(SwapiError)
async def swapi_error_handler(request: Request, exc: SwapiError):
    """Handle errors from SWAPI and return a clear JSON response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
    