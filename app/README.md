# Shortlink API

FastAPI service: create short links, redirect, and record clicks. PostgreSQL in production, SQLite in unit tests.

## Endpoints
| Method | Path | Purpose |
|---|---|---|
| POST | `/links` | Create a link. Body: `{"target_url": "https://..."}` (http/https only, max 2048 chars) |
| GET | `/{code}` | 302 redirect to the target and record a click |
| GET | `/links/{code}/stats` | Total clicks and clicks per day |
| GET | `/healthz` | Liveness (does not touch the database) |
| GET | `/readyz` | Readiness (checks the database) |
| GET | `/metrics` | Prometheus metrics |

## Configuration (environment variables)
| Variable | Default | Meaning |
|---|---|---|
| `SHORTLINK_DATABASE_URL` | local Postgres URL | SQLAlchemy URL |
| `SHORTLINK_BASE_URL` | `http://localhost:8000` | Used to build `short_url` |
| `SHORTLINK_CODE_LENGTH` | `7` | Length of generated codes |

## Run locally with Docker Compose
```bash
cd app
docker compose up --build        # API on http://127.0.0.1:8000, docs at /docs
docker compose down              # stop (add -v to delete the database volume)
```

## Develop and test without Docker
```bash
cd app
python -m venv .venv
.venv/Scripts/pip install -r requirements-dev.txt     # Windows; use .venv/bin/pip elsewhere
.venv/Scripts/python -m pytest
.venv/Scripts/python -m ruff check . && .venv/Scripts/python -m ruff format --check .
```

## Design notes
- App factory (`create_app`), run with `uvicorn --factory shortlink.main:create_app`.
- Migrations are run explicitly (`alembic upgrade head`), never on import. In Kubernetes this becomes a Job / init step.
- `/{code}` is registered last so it cannot shadow fixed routes.
- Metrics use the route template as the label, which keeps cardinality bounded.
- The image is multi-stage and runs as UID 10001 (compatible with `runAsNonRoot`).
