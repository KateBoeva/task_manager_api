# Task Manager API

A REST API for managing tasks and their statuses, built with FastAPI and PostgreSQL.

The project follows a layered architecture (API → services → repositories) with a request-scoped database session injected through FastAPI's dependency system, Pydantic validation, and a fully containerized setup.

## Tech stack

- **Python 3.11**, **FastAPI**, **Uvicorn**
- **PostgreSQL 15**, **SQLAlchemy 2.0** (typed ORM models), **Alembic** for migrations
- **Pydantic v2**, **pydantic-settings** for configuration
- **Docker** / **Docker Compose**
- **pytest** for testing, **Ruff** for linting, **GitHub Actions** for CI

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
- Errors map to proper HTTP status codes: `404` for missing objects, `400`/`409` for foreign key violations, `409` for duplicate names, `422` for invalid input.
- The database schema is managed with Alembic migrations (`migrations/`).
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
| `SQL_ECHO`          | Log SQL queries and their parameters (debugging only) | `false` |

### Run with Docker Compose (recommended)

```bash
docker compose up --build
```

This starts PostgreSQL and the API. The API container waits until the database passes its health check, applies migrations, and then starts.

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

docker compose up -d db          # or use your own PostgreSQL instance
alembic upgrade head
uvicorn app.main:app --reload
```

### Priorities

Priorities do not have API endpoints yet. Migrations create the default ones: `Low`, `Medium` and `High`.

### Migrations

After changing the models, generate and apply a migration:

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

## API

All endpoints accept and return JSON.

### Statuses

| Method   | Endpoint               | Description         | Success | Errors     |
|----------|------------------------|---------------------|---------|------------|
| `GET`    | `/statuses`            | List all statuses   | `200`   |            |
| `GET`    | `/statuses/{id}`       | Get a status by ID  | `200`   | `404`      |
| `POST`   | `/statuses`            | Create a status     | `201`   | `409` (name already exists), `422` |
| `PUT`    | `/statuses/{id}`       | Rename a status     | `200`   | `404`, `409` (name already exists), `422` |
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
migrations/              # Alembic migrations
tests/
├── conftest.py          # pytest fixtures
├── test_migrations.py
├── test_status.py
└── test_task.py
.github/workflows/ci.yml # Lint and tests
Dockerfile
docker-compose.yml
docker-compose.test.yml  # PostgreSQL for tests
pytest.ini               # Test database connection
requirements.txt         # Runtime dependencies
requirements-dev.txt     # Runtime dependencies plus test and lint tools
```

## Testing

```bash
pip install -r requirements-dev.txt
docker compose -f docker-compose.test.yml up -d --wait
pytest
```

The tests run against a dedicated PostgreSQL container (`docker-compose.test.yml`, port `5433`) that stores its data in memory. Its connection settings live in `pytest.ini` and take precedence over `service.env`, so the application code under test cannot reach the main database. The schema is rebuilt from the migrations on every run, and each test runs in a transaction that is rolled back.

## Roadmap

- [x] Tests on an isolated PostgreSQL test database
- [x] Database migrations with Alembic
- [x] CI with GitHub Actions
- [ ] Update and delete endpoints for tasks
- [ ] CRUD endpoints for priorities
- [ ] Pagination and filtering for task lists
- [ ] Authentication
- [ ] Logging
- [ ] AI integration
