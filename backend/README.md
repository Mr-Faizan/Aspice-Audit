# ASPICE Audit — Backend

FastAPI + SQLModel + PostgreSQL backend for the ASPICE continuous assessment tool.

## Requirements

- [Docker](https://www.docker.com/) — runs the full stack (backend, frontend, DB, Adminer)
- [uv](https://docs.astral.sh/uv/) — Python package manager (for local dev outside Docker)

---

## Quick Start (Docker)

```bash
# from the repo root
docker compose watch
```

The backend starts on `http://localhost:8000` and auto-reloads on file changes.

Interactive API docs: `http://localhost:8000/docs`

---

## API Routes

All routes are prefixed with `/api/v1`.

### Auth
| Method | Path | Description |
|---|---|---|
| `POST` | `/login/access-token` | Exchange credentials for JWT |
| `POST` | `/login/test-token` | Verify token |
| `POST` | `/users/signup` | Register new user (with stakeholder role) |

### Audit Sessions (any authenticated user)
| Method | Path | Description |
|---|---|---|
| `POST` | `/audit/sessions/` | Start a new audit session — CMAB selects first question |
| `GET` | `/audit/sessions/` | List own sessions (paginated) |
| `GET` | `/audit/sessions/{id}` | Get session detail |
| `POST` | `/audit/sessions/{id}/answer` | Submit an answer — returns next question or completion |
| `GET` | `/audit/sessions/{id}/results` | Get weakness results for a completed session |

### Question Bank (admin only)
| Method | Path | Description |
|---|---|---|
| `GET` | `/questions/` | List questions with filters (process, level, stakeholder, active) |
| `POST` | `/questions/` | Create question + options + initialise CMAB arm |
| `PATCH` | `/questions/{id}` | Update question fields or replace options |
| `DELETE` | `/questions/{id}` | Soft-delete (sets `is_active=False`) |
| `POST` | `/questions/seed` | Idempotent bulk seed from JSON list |

### Analytics (admin only)
| Method | Path | Description |
|---|---|---|
| `GET` | `/analytics/weaknesses` | Aggregate weakness heatmap across all completed sessions |
| `GET` | `/analytics/users` | Session counts per stakeholder role |
| `GET` | `/analytics/bandit` | CMAB arm performance (pull count, avg reward per question) |

---

## Project Layout

```
backend/
├── app/
│   ├── api/
│   │   ├── main.py              # router registration
│   │   ├── deps.py              # FastAPI dependencies (auth, DB session)
│   │   └── routes/
│   │       ├── audit.py         # audit session endpoints
│   │       ├── questions.py     # question bank (admin)
│   │       ├── analytics.py     # analytics (admin)
│   │       ├── users.py         # user management
│   │       └── login.py         # auth
│   ├── services/
│   │   ├── audit_service.py     # session orchestration (start, answer, complete)
│   │   ├── cmab_engine.py       # LinUCB contextual bandit (select + update arm)
│   │   └── weakness_classifier.py  # score aggregation + top-weakness ranking
│   ├── models.py                # SQLModel DB models + Pydantic schemas
│   ├── crud.py                  # DB helpers
│   ├── seed_questions.py        # one-time question bank seed script
│   └── core/
│       ├── config.py            # settings (env vars)
│       ├── security.py          # password hashing, JWT
│       └── db.py                # engine + session factory
└── alembic/                     # DB migrations
```

---

## Database Models

| Table | Purpose |
|---|---|
| `user` | Stakeholders and admins; carries `stakeholder_role` |
| `auditquestion` | Question bank — one row per question |
| `auditoption` | 5 weighted options (A–E, weight 0–4) per question |
| `auditsession` | One assessment run per user; tracks progress and status |
| `auditresponse` | Each answer submitted during a session |
| `weaknessresult` | Computed scores + top weaknesses, one per completed session |
| `banditarmstate` | LinUCB arm state (A matrix, b vector) per question |

---

## Migrations

```bash
# inside the running backend container
docker compose exec backend bash

# generate a new migration after model changes
alembic revision --autogenerate -m "describe the change"

# apply pending migrations
alembic upgrade head
```

---

## Running Tests

```bash
docker compose exec backend bash scripts/tests-start.sh

# stop on first failure
docker compose exec backend bash scripts/tests-start.sh -x

# run a specific file without the DB-dependent conftest
docker compose exec backend bash -c "pytest tests/services/test_cmab_engine.py --noconftest -v"
```

Tests live under `backend/tests/`. Services are fully unit-tested (56 tests, all passing).

---

## Seeding the Question Bank

```bash
docker compose exec backend python app/seed_questions.py
```

This seeds 42 questions across SWE.1–SWE.6 (L1/L2/L3) idempotently. Alternatively use `POST /questions/seed` with a JSON payload through the admin UI or API docs.

---

## Local Dev (without Docker)

```bash
cd backend
uv sync
source .venv/bin/activate
# set env vars from .env
fastapi run --reload app/main.py
```
