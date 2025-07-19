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

---

## 2. CLI Client

### Run in Docker Compose
You can exec into the CLI container:
```bash
docker-compose exec cli bash
# Then run CLI commands as below
```

### Run Locally (Recommended)
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
- `API_BASE_URL` (default: `http://backend:8000` in Docker, or `http://localhost:8000` locally)

---

## 4. Project Structure
```
starwars_app/
  backend/         # FastAPI backend
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

