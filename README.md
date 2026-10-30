# Task Manager API

A REST API for managing tasks and their statuses, built with FastAPI and PostgreSQL.

The project follows a layered architecture (API → services → repositories) with a request-scoped database session injected through FastAPI's dependency system, Pydantic validation, and a fully containerized setup.

## Tech stack

- **Python 3.11**, **FastAPI**, **Uvicorn**
- **PostgreSQL 15**, **SQLAlchemy 2.0** (typed ORM models)
- **Pydantic v2**, **pydantic-settings** for configuration
- **Docker** / **Docker Compose**
- **pytest** for testing

## Architecture

```
HTTP request
   │
   ▼
app/main.py          API layer: routing, request/response schemas, HTTP errors
   │  Depends(get_db) – one SQLAlchemy session per request
   ▼
app/services/        Business logic (StatusService, TaskService)
   │
   ▼
app/repos/           Data access (StatusRepo, TaskRepo)
   │
   ▼
PostgreSQL
```

- Request and response bodies are validated with Pydantic schemas (`app/schemas.py`).
- Errors map to proper HTTP status codes: `404` for missing objects, `400`/`409` for foreign key violations, `422` for invalid input.
- Database tables are created on application startup via the FastAPI lifespan hook.
- Configuration is read from environment variables or the `service.env` file.

## Getting started

### Configuration

```bash
cp service.env.example service.env
```

Edit `service.env` and set your database credentials:

| Variable            | Description       | Default     |
|---------------------|-------------------|-------------|
| `POSTGRES_USER`     | Database user     | —           |
| `POSTGRES_PASSWORD` | Database password | —           |
| `POSTGRES_DB`       | Database name     | —           |
| `POSTGRES_HOST`     | Database host     | `localhost` |
| `POSTGRES_PORT`     | Database port     | `5432`      |

### Run with Docker Compose (recommended)

```bash
docker compose up --build
```

This starts PostgreSQL and the API. The API container waits until the database passes its health check before starting.

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

docker compose up -d db          # or use your own PostgreSQL instance
uvicorn app.main:app --reload
```

### Seed priorities

Priorities do not have API endpoints yet. Before you create tasks, add them to the database:

```bash
docker compose exec db sh -c \
  'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "INSERT INTO priority (name) VALUES ('"'"'Low'"'"'), ('"'"'Medium'"'"'), ('"'"'High'"'"');"'
```

## API

All endpoints accept and return JSON.

### Statuses

| Method   | Endpoint               | Description         | Success | Errors     |
|----------|------------------------|---------------------|---------|------------|
| `GET`    | `/statuses`            | List all statuses   | `200`   |            |
| `GET`    | `/statuses/{id}`       | Get a status by ID  | `200`   | `404`      |
| `POST`   | `/statuses`            | Create a status     | `201`   | `422`      |
| `PUT`    | `/statuses/{id}`       | Rename a status     | `200`   | `404`, `422` |
| `DELETE` | `/statuses/{id}`       | Delete a status     | `204`   | `404`, `409` (status is used by tasks) |

### Tasks

| Method | Endpoint       | Description        | Success | Errors |
|--------|----------------|--------------------|---------|--------|
| `GET`  | `/tasks`       | List all tasks     | `200`   |        |
| `GET`  | `/tasks/{id}`  | Get a task by ID   | `200`   | `404`  |
| `POST` | `/tasks`       | Create a task      | `201`   | `400` (unknown status or priority), `422` |

### Example

```bash
curl -X POST http://localhost:8000/statuses \
  -H "Content-Type: application/json" \
  -d '{"name": "To Do"}'
# {"id": 1, "name": "To Do"}

curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Write README", "description": "In English", "status_id": 1, "priority_id": 1}'
# {"id": 1, "title": "Write README", "description": "In English",
#  "status_id": 1, "priority_id": 1, "created_at": "2026-10-30T20:33:53.558098Z"}
```

## Project structure

```
app/
├── main.py              # FastAPI app, routes, lifespan
├── models.py            # SQLAlchemy models: Task, Status, Priority
├── schemas.py           # Pydantic request/response schemas
├── database.py          # Engine, session factory, get_db dependency
├── settings.py          # Configuration (pydantic-settings)
├── repos/               # Data access layer
│   ├── status_repo.py
│   └── task_repo.py
└── services/            # Business logic layer
    ├── status_service.py
    └── task_service.py
tests/
├── conftest.py          # pytest fixtures
└── test_status.py
Dockerfile
docker-compose.yml
```

## Testing

```bash
pytest
```

The test suite is a work in progress. The next step is to run the tests against a dedicated PostgreSQL test database.

## Roadmap

- [ ] Tests on an isolated PostgreSQL test database
- [ ] Update and delete endpoints for tasks
- [ ] CRUD endpoints for priorities
- [ ] Database migrations with Alembic
- [ ] Pagination and filtering for task lists
- [ ] Authentication
- [ ] Logging
- [ ] AI integration

## License

MIT
