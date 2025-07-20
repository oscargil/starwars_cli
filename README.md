# Star Wars CLI & FastAPI Service

Explore Star Wars People and Planets from the command line and via a REST API, powered by FastAPI and SWAPI.

## Features
- FastAPI backend with `/people` and `/planets` endpoints
- Query params: `page`, `search`, `sort_by`
- Proxies SWAPI, applies pagination, filtering, and sorting
- Python CLI client (Typer) to list/search/sort people and planets
- Dockerized for easy setup

---

## 1. FastAPI Service

### Run with Docker Compose
```bash
docker-compose up --build
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

**Example:**
```
GET /people?page=1&search=luke&sort_by=name
```

### Mock AI Insight Endpoint
- `GET /simulate-ai-insight`

Returns a fake “AI” description for a given person or planet name. Useful for demo or testing.

#### Query Parameters
- `type` (string, required): `person` or `planet`
- `name` (string, required): Name of the person or planet

**Example:**
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

---

## 2. CLI Client

### Run in Docker Compose
You can exec into the CLI container:
```bash
docker-compose exec starwars_cli bash
# Then run CLI commands as below
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

---

## 3. Environment Variables

- `API_BASE_URL`:
  - In Docker (from another service/container): `http://backend:8000`
  - On your local machine (with Docker Compose): `http://localhost:6969`
  - On your local machine (running backend directly): `http://localhost:8000`

---

## 4. Project Structure
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

## 5. Example API Usage
```bash
curl "http://localhost:6969/people?page=1&search=skywalker&sort_by=name"
curl "http://localhost:6969/planets?page=2&sort_by=diameter"
```

---

## 6. Backend Performance: Caching

To improve performance and reduce latency, the backend uses an in-memory cache for SWAPI responses. This means that repeated queries for the same resource and search term are served much faster, reducing the number of requests to SWAPI and improving user experience.

- **How it works:**
  - The cache is implemented using [`async_lru`](https://pypi.org/project/async-lru/).
  - Up to 64 unique queries are cached in memory.
  - The cache is automatically cleared when the server restarts, or can be cleared programmatically if needed.

This approach provides a significant speed boost for repeated queries and helps avoid hitting SWAPI rate limits.

---

## 7. Logging

Backend activity, such as search and sort requests, is logged for monitoring and debugging purposes.

- Logs are written to `backend/logs/starwars.log` (the directory is created automatically).
- The log file is excluded from git, but the directory is included for convenience.
- Logs are output both to the file and to the console.
- In Docker, map the `backend/logs` directory to your host to persist and access logs outside the container.
- Example log entry:
  ```
  2024-05-01 12:34:56,789 INFO Search/Sort request: resource=people, search=luke, sort_by=name, page=1
  ```
- To view logs locally, check `backend/logs/starwars.log`.
- In Docker, use a mapped volume or run:
  ```bash
  docker-compose exec starwars_backend cat backend/logs/starwars.log
  ```

