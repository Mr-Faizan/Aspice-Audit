# ASPICE Audit — Continuous Process Assessment Tool

A full-stack web application that automates **Automotive SPICE (ASPICE)** process assessment for the SWE.1–SWE.6 software engineering process group. Uses a **Contextual Multi-Armed Bandit (LinUCB)** to personalise question selection per stakeholder and session, then classifies process weaknesses from the answers.

**Master's Thesis project** — Recommendation System for ASPICE Process Assessment.

---

## What It Does

1. A stakeholder logs in and selects "Start Audit"
2. The LinUCB engine selects the most informative question for that user's role and session history
3. The stakeholder answers 12 questions one at a time
4. The system computes a weakness score for each SWE process × capability level cell (6 processes × 3 levels = 18 cells)
5. Results are shown as a radar chart, a colour-coded heatmap, and a ranked weakness list
6. The bandit arm is updated with the observed reward — the system learns across sessions

Admins can manage the question bank, view aggregate heatmaps across all users, and inspect CMAB arm performance.

---

## ASPICE Processes Covered

| Process | Name |
|---|---|
| SWE.1 | Software Requirements Analysis |
| SWE.2 | Software Architectural Design |
| SWE.3 | Software Detailed Design and Unit Construction |
| SWE.4 | Software Unit Verification |
| SWE.5 | Software Integration and Integration Test |
| SWE.6 | Software Qualification Test |

**Capability levels:** L1 (Performed) · L2 (Managed) · L3 (Established)

**Stakeholder roles:** Software Developer · Software Architect · Project Manager · QA Engineer · Test Engineer · Team Lead · ASPICE Assessor

---

## Technology Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI + Python 3.12 |
| ORM / DB | SQLModel + PostgreSQL |
| ML Engine | NumPy — LinUCB contextual bandit |
| Frontend | React 18 + TypeScript + Vite |
| Routing | TanStack Router (file-based) |
| API Client | `@hey-api/openapi-ts` (generated from OpenAPI spec) |
| UI | Tailwind CSS + shadcn/ui |
| Auth | JWT (access tokens) |
| Dev | Docker Compose with hot reload |

---

## Quick Start

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose

### Run

```bash
git clone <repo-url> aspice-audit
cd aspice-audit
cp .env.example .env        # edit DB credentials and SECRET_KEY
docker compose watch
```

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| Adminer (DB UI) | http://localhost:8080 |

### Seed the question bank

```bash
docker compose exec backend python app/seed_questions.py
```

This inserts 42 questions across all SWE processes and levels (idempotent — safe to run multiple times).

### Create an admin user

Use the API docs at `/docs` to `POST /api/v1/users/` with `is_superuser: true`, or use the Adminer DB UI to set `is_superuser = true` on an existing user.

---

## Repository Layout

```
aspice-audit/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/routes/      # audit, questions, analytics, users, login
│   │   ├── services/        # audit_service, cmab_engine, weakness_classifier
│   │   ├── models.py        # DB models + Pydantic schemas
│   │   ├── crud.py          # DB helpers
│   │   └── seed_questions.py
│   └── tests/               # pytest unit tests (56 tests)
├── frontend/                # React application
│   └── src/
│       ├── routes/          # TanStack Router file-based routes
│       │   └── _layout/
│       │       ├── quizzes/     # Audits list (start / continue / view results)
│       │       ├── audit/       # Session flow + results page
│       │       ├── history.tsx  # All sessions table
│       │       ├── dashboard.tsx # Admin analytics dashboard
│       │       └── admin-quizzes.tsx # Admin question bank manager
│       └── client/          # Generated typed API client
├── Architecture.md          # System design and component breakdown
└── ToDoList.md              # Implementation task tracker
```

---

## Key Design Decisions

- **No global "current question" endpoint** — the frontend stores the current question in `sessionStorage` after each API call, avoiding a round-trip and keeping the backend stateless per request.
- **LinUCB α = 1.0** — balanced exploration/exploitation; tunable via the `alpha` parameter in `cmab_engine.py`.
- **Soft delete for questions** — deactivating a question sets `is_active = False` and keeps the `BanditArmState` intact for historical analysis.
- **Reward function** — base reward = `option.weight / 4`, with a +0.2 coverage bonus for the first question asked in a process, clamped to [0, 1].
- **23-dimensional context vector** — 7 role dims + 1 progress + 6 process coverage + 3 level coverage + 6 running weakness scores per process.

---

## Architecture

See [Architecture.md](Architecture.md) for the full system design, database schema, CMAB algorithm details, API design, and frontend component breakdown.
