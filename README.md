# Star Wars CLI & FastAPI Service

Explore Star Wars People and Planets from the command line and via a REST API, powered by FastAPI and SWAPI.

---

## Features
- FastAPI backend with `/people` and `/planets` endpoints
- Query params: `page`, `search`, `sort_by`
- Proxies SWAPI, applies pagination, filtering, and sorting
- Python CLI client (Typer) to list/search/sort people and planets
- Dockerized for easy setup

---

## 1. FastAPI Service

**Purpose:**  
Provides a REST API to explore Star Wars people and planets, with pagination, search, and sorting.

### Build Docker Images
Before running any services with Docker Compose, you must build the images:
```bash
docker compose build
```

### Run with Docker Compose
**Important:**
If you run `docker compose up` (or `docker-compose up`) without specifying services, **all defined services will start, including the `test` service** (which will run the tests and then exit). To start only the application (backend and cli), run:

```bash
docker compose up backend cli
```

- The API will be available at: [http://localhost:6969](http://localhost:6969)

### Run Locally (without Docker)
```bash
# Install dependencies
pip install -r requirements.txt

# Start FastAPI (default port 8000)
uvicorn backend.main:app --reload
```
- The API will be available at: [http://localhost:8000](http://localhost:8000)

### API Endpoints
- `GET /people`
- `GET /planets`

#### Query Parameters
- `page` (integer, default: 1) – Returns 10 items per page
- `search` (string) – Case-insensitive partial match on the name field
- `sort_by` (string) – Sort by any attribute (e.g., name, created)

#### Example Usage
```
GET /people?page=1&search=luke&sort_by=name
```

### Mock AI Insight Endpoint
- `GET /simulate-ai-insight`

Returns a fake “AI” description for a given person or planet name. Useful for demo or testing.

#### Query Parameters
- `type` (string, required): `person` or `planet`
- `name` (string, required): Name of the person or planet

#### Example
```
curl "http://localhost:8000/simulate-ai-insight?type=person&name=Luke%20Skywalker"
```
Response:
```
{
  "type": "person",
  "name": "Luke Skywalker",
  "ai_description": "This person named 'Luke Skywalker' is truly remarkable. According to our advanced AI, Luke Skywalker is destined to play a pivotal role in the galaxy!"
}
```

### Backend Performance: Caching

**Purpose:**  
Improve performance and reduce latency by caching SWAPI responses.

#### How it Works
- The cache is implemented using [`async_lru`](https://pypi.org/project/async-lru/).
- Up to 64 unique queries are cached in memory.
- The cache is automatically cleared when the server restarts, or can be cleared programmatically if needed.

#### Notes
- This approach provides a significant speed boost for repeated queries and helps avoid hitting SWAPI rate limits.

### Logging

**Purpose:**  
Track and monitor backend activity for debugging and auditing.

#### Log Locations
- Logs are written to `backend/logs/starwars.log` (the directory is created automatically).
- The log file is excluded from git, but the directory is included for convenience.
- Logs are output both to the file and to the console.

#### Example Log Entry
```
2024-05-01 12:34:56,789 INFO Search/Sort request: resource=people, search=luke, sort_by=name, page=1
```

### Example API Usage

**Purpose:**  
Demonstrate how to interact with the API using curl.

#### Example curl Commands
```bash
curl "http://localhost:6969/people?page=1&search=skywalker&sort_by=name"
curl "http://localhost:6969/planets?page=2&sort_by=diameter"
```

### Notes
- The backend service is exposed on port 8000 inside Docker, mapped to 6969 on your host.
- All endpoints support pagination, search, and sorting as described above.

---

## Interactive API Documentation (FastAPI)

The API provides interactive, auto-generated documentation via FastAPI:

- **Swagger UI:** [http://localhost:6969/docs](http://localhost:6969/docs)
- **ReDoc:** [http://localhost:6969/redoc](http://localhost:6969/redoc)

These interfaces let you visually explore and test all API endpoints directly from your browser.

---

## 2. CLI Client

**Purpose:**  
A command-line interface to interact with the Star Wars API, allowing you to list, search, and sort people and planets.

### Build Docker Images
Before running the CLI in Docker Compose, make sure the images are built:
```bash
docker compose build
```

### Run in Docker Compose
To use the CLI inside Docker Compose, first make sure the backend service is running (see section 1). Then, you can open a terminal inside the CLI container:

```bash
docker compose up backend cli  # (if not already running)
docker compose exec cli bash
# Now you can run CLI commands as shown below
```

### Run Locally
```bash
cd cli
pip install -r ../requirements.txt
python main.py --help
```

### Example Commands
List people (first page):
```bash
python main.py list-people
```

List planets, page 2, sorted by name:
```bash
python main.py list-planets --page 2 --sort-by name
```

Search people by name:
```bash
python main.py list-people --search luke
```

### Notes
- By default, the CLI will connect to `http://localhost:6969` if run outside Docker, and to `http://backend:8000` if run inside Docker Compose (as set in `docker-compose.yml`).
- You can override this by setting the `API_BASE_URL` environment variable in your environment or `.env` file.

---

## 3. Environment Variables

**Purpose:**  
Configure the backend and CLI for flexible deployment (local, Docker, or cloud providers).

### List of Variables
- `API_BASE_URL`:  
  - Default for CLI in Docker Compose: `http://backend:8000` (set in `docker-compose.yml`)
  - Default for CLI outside Docker: `http://localhost:6969`
  - You can override this in your environment or `.env` file.
- `SWAPI_BASE_URL`: Base URL for the Star Wars API proxy (default: `https://swapi.dev/api`).
- `PAGE_SIZE`: Number of items per page for pagination (default: `10`). Applies to both backend and CLI.
- `CACHE_SIZE`: Number of unique SWAPI queries to cache in memory (default: `64`).
- `LOG_LEVEL`: Logging level for backend logs (default: `INFO`).
- `PORT`: Port for the FastAPI backend (default: `8000`). Set this when running uvicorn, e.g. `uvicorn backend.main:app --port $PORT`.
- `REQUEST_TIMEOUT`: Timeout (in seconds) for CLI HTTP requests (default: `10`).

### Example .env File
```env
# API base URL for CLI
API_BASE_URL=http://localhost:6969

# SWAPI proxy base URL
SWAPI_BASE_URL=https://swapi.dev/api

# Items per page
PAGE_SIZE=10

# Cache size for SWAPI queries
CACHE_SIZE=64

# Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Backend port (used when running uvicorn)
PORT=8000

# CLI request timeout (seconds)
REQUEST_TIMEOUT=10
```

### Notes
- All environment variables have sensible defaults. The application will work even if no `.env` file is present.

---

## 4. Project Structure

**Purpose:**  
Overview of the main directories and files in the project.

### Directory Tree
```
starwars_app/
  backend/         # FastAPI backend
    logs/          # Backend log files (not tracked by git)
  cli/             # Python CLI client (Typer)
  requirements.txt # Shared dependencies
  Dockerfile       # For backend & CLI
  docker-compose.yml
```

---

## 5. Running Tests (Docker Compose)

**Purpose:**  
Run all unit tests for the backend and CLI in an isolated environment.

### Build Docker Images
Before running the tests, make sure the images are built:
```bash
docker compose build
```

### Run Tests
To execute all unit tests (without starting backend or CLI services):
```
```