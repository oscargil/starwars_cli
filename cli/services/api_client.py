import requests
from typing import Optional, Dict, Any
import os

REQUEST_TIMEOUT = float(os.environ.get("REQUEST_TIMEOUT", 10))

class ApiError(Exception):
    """Exception for API errors."""
    pass

class ApiClient:
    """Client for interacting with the Star Wars FastAPI backend."""
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get_resource(self, resource: str, page: int = 1, sort_by: Optional[str] = None, search: Optional[str] = None) -> Dict[str, Any]:
        """Fetch a paginated resource from the API."""
        params = {"page": page}
        if sort_by:
            params["sort_by"] = sort_by
        if search:
            params["search"] = search
        url = f"{self.base_url}/{resource}"
        try:
            response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ApiError(f"HTTP error: {e.response.status_code} {e.response.reason}") from e
        except requests.exceptions.ConnectionError as e:
            raise ApiError("Failed to connect to the API server.") from e
        except requests.exceptions.Timeout as e:
            raise ApiError("Request to API server timed out.") from e
        except requests.exceptions.RequestException as e:
            raise ApiError(f"API request error: {str(e)}") from e
        try:
            return response.json()
        except ValueError as e:
            raise ApiError("Invalid JSON response from API.") from e 