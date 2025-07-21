import httpx
from typing import Optional, List, Dict, Any
from backend.services.exceptions import SwapiError
from async_lru import alru_cache
import os

SWAPI_BASE_URL = os.getenv("SWAPI_BASE_URL", "https://swapi.dev/api")
PAGE_SIZE = int(os.getenv("PAGE_SIZE", 10))
CACHE_SIZE = int(os.getenv("CACHE_SIZE", 64))

class SwapiService:
    """Service for fetching, sorting, and paginating Star Wars data from SWAPI."""
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    @alru_cache(maxsize=CACHE_SIZE)
    async def fetch_all(self, resource: str, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch all results for a resource from SWAPI, optionally filtered by search. Cached for performance."""
        all_results = []
        url = f"{SWAPI_BASE_URL}/{resource}/"
        params = {"search": search} if search else None
        first = True
        while url:
            try:
                if first:
                    response = await self.client.get(url, params=params)
                    first = False
                else:
                    response = await self.client.get(url)
                response.raise_for_status()
                data = response.json()
                all_results.extend(data.get("results", []))
                url = data.get("next")
            except httpx.HTTPStatusError as e:
                raise SwapiError(f"SWAPI returned HTTP error: {e.response.status_code}", status_code=e.response.status_code)
            except httpx.RequestError as e:
                raise SwapiError("Failed to connect to SWAPI.") from e
            except Exception as e:
                raise SwapiError("Unexpected error while fetching data from SWAPI.") from e
        return all_results

    def clear_cache(self):
        """Clear the SWAPI fetch cache (for testing or admin use)."""
        self.fetch_all.cache_clear()

    def sort_data(self, data: List[Dict[str, Any]], sort_by: Optional[str]) -> List[Dict[str, Any]]:
        """Sort data by the specified attribute if provided. Items missing the key are placed at the end."""
        if sort_by:
            data.sort(key=lambda item: (sort_by not in item, str(item.get(sort_by, ""))))
        return data

    def paginate(self, data: List[Dict[str, Any]], page: int, base_url: str) -> Dict[str, Any]:
        """Paginate the data and return a paginated response."""
        total_items = len(data)
        start_index = (page - 1) * PAGE_SIZE
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