# Account Service

A small Flask-based RESTful microservice providing CRUD operations for Account resources and a health endpoint.

## Overview

This repository implements an Account REST API built with Flask and SQLAlchemy. It includes unit tests, a Dockerfile for containerization, Kubernetes deployment manifests, and a Tekton pipeline for CI/CD.

- Application entrypoint: the Flask app instance is exposed as `service:app` ([service/**init**.py](service/__init__.py)).
- Persistence: SQLAlchemy with PostgreSQL (configurable via environment).
- Tests: nose-based test suite in `tests/`.

## Features

- CRUD for Account resources: create, list, read, update, delete.
- Health endpoint (`/health`) and root index (`/`).
- Database initialization CLI command: `flask db-create`.
- Unit tests and test factories for reproducible test data.
- Dockerfile for production container, Kubernetes manifests for deployment.
- Tekton pipeline example for CI/CD.

## Tech Stack

- Python 3.9 (Docker base image: `python:3.9-slim`)
- Flask
- Flask-SQLAlchemy / SQLAlchemy
- PostgreSQL (psycopg2)
- Gunicorn (WSGI server)
- Testing: nose, factory_boy
- Lint/format: flake8, pylint, black
- Containerization: Docker
- Orchestration / CI: Kubernetes manifests (`deploy/`) and Tekton pipeline (`tekton/`)
- License: Apache-2.0 ([LICENSE](LICENSE))

## Repository Structure (key files)

- [service/](service/)
  - [service/**init**.py](service/__init__.py) — app factory and initialization
  - [service/routes.py](service/routes.py) — HTTP endpoints (CRUD + health)
  - [service/models.py](service/models.py) — SQLAlchemy models and persistence
  - [service/config.py](service/config.py) — configuration via environment variables
  - [service/common/cli_commands.py](service/common/cli_commands.py) — `flask` CLI helpers
  - [service/common/error_handlers.py](service/common/error_handlers.py) — JSON error handlers
- [tests/](tests/) — unit tests and factories
  - [tests/test_routes.py](tests/test_routes.py)
  - [tests/factories.py](tests/factories.py)
- Dockerfile — container image
- Procfile — Heroku/Procfile-compatible startup
- requirements.txt — pinned Python dependencies
- deploy/
  - [deploy/deployment.yaml](deploy/deployment.yaml) — Deployment template (IMAGE_NAME_HERE)
  - [deploy/service.yaml](deploy/service.yaml) — ClusterIP Service (port 8080)
- tekton/
  - [tekton/pipeline.yaml](tekton/pipeline.yaml) — Tekton pipeline (lint, tests, build, deploy)
- LICENSE — Apache 2.0 license

Small tree (top-level):

```
.
├─ service/
│  ├─ __init__.py
│  ├─ routes.py
│  ├─ models.py
│  └─ common/
├─ tests/
│  ├─ test_routes.py
│  └─ factories.py
├─ Dockerfile
├─ Procfile
├─ requirements.txt
├─ deploy/
└─ tekton/
```

## Prerequisites

- Python 3.9 (recommended to match Docker base image)
- PostgreSQL (for local development or tests using a real DB)
- pip
- Docker (if building/running container)
- For Tekton pipeline: Tekton installed on a Kubernetes/OpenShift cluster (pipeline uses ClusterTasks like `buildah`, `openshift-client`)

## Quickstart

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set a PostgreSQL connection (either via `DATABASE_URI` or individual env vars). Example (local Postgres default values used by the app if not set):

```bash
export DATABASE_URI='postgresql://postgres:postgres@localhost:5432/postgres'
# or set individual parts (app will construct DATABASE_URI if not provided)
export DATABASE_HOST=localhost
export DATABASE_USER=postgres
export DATABASE_PASSWORD=postgres
export DATABASE_NAME=postgres
```

3. Run the app (development / production via gunicorn):

```bash
# using gunicorn (binds to 0.0.0.0:8080 per Dockerfile)
gunicorn --bind=0.0.0.0:8080 service:app

# or (when using Procfile runner like honcho/foreman):
honcho start
```

4. Verify health:

```bash
curl -sS http://localhost:8080/health
# -> {"status":"OK"}
```

## Local Development

### Install

Use the Quickstart install step (`pip install -r requirements.txt`). Consider a virtualenv.

### Run

- Gunicorn (production-like):
  ```bash
  gunicorn --bind=0.0.0.0:8080 service:app
  ```
- Flask CLI is available (module sets up `app` and registers CLI commands). To use Flask CLI:
  ```bash
  export FLASK_APP=service
  flask --help
  # Example: recreate DB tables (development only)
  flask db-create
  ```

### Environment Variables / Configuration

Configuration resides in [service/config.py](service/config.py). Primary variables:

- `DATABASE_URI` — full SQLAlchemy URI (e.g. `postgresql://user:pass@host:5432/dbname`). If unset, the app builds the URI from:
  - `DATABASE_USER` (default `postgres`)
  - `DATABASE_PASSWORD` (default `postgres`)
  - `DATABASE_NAME` (default `postgres`)
  - `DATABASE_HOST` (default `localhost`)
- `SECRET_KEY` — Flask secret (default `s3cr3t-key-shhhh`)

Set these in your shell or via your container/orchestration secrets.

## Testing

Run unit tests with nose as used in the repo:

```bash
nosetests -v --with-spec --spec-color
```

Coverage (example):

```bash
coverage run -m nose && coverage report -m
```

Notes:

- Tests rely on a configured `DATABASE_URI` (see `tests/test_routes.py` for how `DATABASE_URI` is read). By default tests will use `postgresql://postgres:postgres@localhost:5432/postgres` if `DATABASE_URI` is not set.

## Linting / Formatting

- Flake8:

```bash
flake8 .
```

- Black (format):

```bash
black .
```

- Pylint:

```bash
pylint service
```

The Tekton pipeline includes a lint task configured to run flake8 with specific args (`--max-complexity=10`, `--max-line-length=127`).

## Docker

Build and run the image using the provided `Dockerfile` (exposes port 8080):

```bash
docker build -t accounts:latest .
docker run -e DATABASE_URI='postgresql://postgres:postgres@db:5432/postgres' -p 8080:8080 accounts:latest
```

The container command is `gunicorn --bind=0.0.0.0:8080 service:app` (see `Dockerfile`).

## Kubernetes / OpenShift

Manifests are in `deploy/`:

- [deploy/deployment.yaml](deploy/deployment.yaml) — deployment template referencing `IMAGE_NAME_HERE` and using env vars/Secrets for DB credentials.
- [deploy/service.yaml](deploy/service.yaml) — ClusterIP service exposing port 8080.

The deployment expects a Kubernetes Secret (name `postgresql`) with keys:

- `database-name`
- `database-password`
- `database-user`

Tekton pipeline (`tekton/pipeline.yaml`) contains a `deploy` task that replaces `IMAGE_NAME_HERE` with the built image and applies the manifests.

## CI/CD

A Tekton pipeline example is provided at [tekton/pipeline.yaml](tekton/pipeline.yaml). It defines tasks for:

- clone
- lint (flake8)
- tests (nose)
- build (buildah)
- deploy (openshift-client)

Notes:

- The pipeline references ClusterTasks such as `git-clone`, `flake8`, `nose`, `buildah`, and `openshift-client`. Ensure these tasks are available in your Tekton cluster.

## API Documentation (endpoints)

Primary endpoints (defined in [service/routes.py](service/routes.py)):

- GET /health — health check
- GET / — index (service name/version)
- POST /accounts — create an Account (JSON)
- GET /accounts — list Accounts
- GET /accounts/<id> — get Account by id
- PUT /accounts/<id> — update Account
- DELETE /accounts/<id> — delete Account

Example curl calls:

```bash
# Health
curl -i http://localhost:8080/health

# Create an account
curl -i -X POST http://localhost:8080/accounts \
	-H 'Content-Type: application/json' \
	-d '{"name":"Alice","email":"alice@example.com","address":"123 Main St"}'

# List accounts
curl -i http://localhost:8080/accounts
```

Payload fields (see [service/models.py](service/models.py)):

- `name` (string, required)
- `email` (string, required)
- `address` (string, required)
- `phone_number` (string, optional)
- `date_joined` (ISO date, optional — defaults to today)

## Troubleshooting

- Database connection errors: verify `DATABASE_URI` or individual DB env vars and that PostgreSQL is reachable on port 5432.
- Missing migration system: this project uses `db.create_all()` (no Alembic migrations included). Use `flask db-create` for dev to recreate tables.
- Tests fail locally: ensure `DATABASE_URI` in your environment points to a test Postgres instance and that the database is accessible.
- Tekton deploy fails: ensure referenced ClusterTasks exist and `oc`/`kubectl` credentials are configured in the pipeline environment.

## Contributing

- No `CONTRIBUTING.md` found; follow standard fork-and-PR workflow.
- The repository is licensed under Apache License 2.0 (see [LICENSE](LICENSE)).

## Security

- Secrets are expected to be provided via environment variables or Kubernetes Secrets (see `deploy/deployment.yaml` which references `postgresql` secret).
- Do not commit production credentials to the repository.

## License

Apache License, Version 2.0 — see [LICENSE](LICENSE).

## Assumptions / TODO

- No `.env.example` or example secrets file present — consider adding one for local development.
- Tekton pipeline references ClusterTasks (`git-clone`, `flake8`, `nose`, `buildah`, `openshift-client`) which are not included in this repo — ensure they exist in your Tekton environment or provide custom tasks.
- `deploy/deployment.yaml` contains placeholder `IMAGE_NAME_HERE`; CI/CD (or manual step) must replace it with your built image.
- The repository `README.md` was empty/whitespace initially; this document was generated by inspecting the code and manifests in the repository.
