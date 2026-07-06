# ASPICE Audit — System Architecture

**Application:** ASPICE Audit  
**Thesis Title:** Recommendation System for ASPICE Process Assessment  
**Stack:** FastAPI · React · SQLModel · PostgreSQL · Docker

---

## Table of Contents

1. [Background](#1-background)
2. [Layered Architecture Overview](#2-layered-architecture-overview)
3. [Database Schema](#3-database-schema)
4. [CMAB Engine](#4-cmab-engine-contextual-multi-armed-bandit)
5. [Weakness Classifier](#5-weakness-classifier)
6. [API Design](#6-api-design)
7. [Frontend Design](#7-frontend-design)
8. [Key Design Decisions](#8-key-design-decisions)
9. [Python Package Layout](#9-python-package-layout)
10. [Migration Path](#10-migration-path-from-current-code)

---

## 1. Background

Automotive SPICE (ASPICE) is a process assessment model used by car OEMs to evaluate how well a supplier develops software and systems.

This application makes ASPICE useful in everyday development by continuously monitoring how well the SWE.1–SWE.6 processes are working. A Machine Learning algorithm (Contextual Multi-Armed Bandit) learns which questions are the most informative and selects them automatically. The result is a weakness classification showing where software process weaknesses exist.

### ASPICE Processes Covered

| Process | Name |
|---|---|
| SWE.1 | Software Requirements Analysis |
| SWE.2 | Software Architectural Design |
| SWE.3 | Software Detailed Design and Unit Construction |
| SWE.4 | Software Unit Verification |
| SWE.5 | Software Integration and Integration Test |
| SWE.6 | Software Qualification Test |

### ASPICE Capability Levels

| Level | Name |
|---|---|
| L1 | Performed |
| L2 | Managed |
| L3 | Established |

### Stakeholder Roles

- Software Developer
- Software Architect
- Project Manager
- QA Engineer
- Test Engineer
- Team Lead
- ASPICE Assessor

---

## 2. Layered Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                      │
│              React + TypeScript + TanStack Router           │
│   Auth  │  Audit Session  │  Results  │  Admin  │ History  │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS / REST JSON
┌──────────────────────────▼──────────────────────────────────┐
│                        API LAYER                            │
│                    FastAPI  /api/v1                         │
│   /auth  │  /audit  │  /questions  │  /results  │  /admin  │
└──────────────────────────┬──────────────────────────────────┘
                           │
          ┌────────────────┼──────────────────┐
          │                │                  │
┌─────────▼──────┐ ┌───────▼──────┐ ┌────────▼──────┐
│ Business Logic │ │  CMAB Engine │ │   Classifier  │
│    Service     │ │   (LinUCB)   │ │   (Weakness)  │
│ Audit Session  │ │ Question     │ │ Score per     │
│ CRUD/Workflow  │ │ Selection    │ │ SWE.1–SWE.6   │
└─────────┬──────┘ └───────┬──────┘ └────────┬──────┘
          │                │                  │
┌─────────▼────────────────▼──────────────────▼──────┐
│                     DATA LAYER                      │
│           SQLModel + PostgreSQL via Alembic         │
│   Users  │  Questions  │  Sessions  │  Responses   │
│          │  BanditState │  Results  │              │
└─────────────────────────────────────────────────────┘
```

### Infrastructure

```
┌──────────────────────────────────────────────────────────┐
│                    Docker Compose                        │
│                                                          │
│  ┌───────────┐  ┌───────────┐  ┌────────┐  ┌────────┐  │
│  │  Frontend │  │  Backend  │  │  DB    │  │Adminer │  │
│  │  Node/    │  │  FastAPI  │  │Postgres│  │  GUI   │  │
│  │  Vite     │  │  :8001    │  │  :5433 │  │  :8080 │  │
│  │  :5173    │  │           │  │        │  │        │  │
│  └───────────┘  └───────────┘  └────────┘  └────────┘  │
│                       ▲                                  │
│               Traefik (production)                       │
│           api.{domain} / dashboard.{domain}              │
└──────────────────────────────────────────────────────────┘
```

---

## 3. Database Schema

### What Changes from Current Models

The existing generic `Quiz` / `Question` / `QuizAttempt` tables are **replaced** by ASPICE-specific models. `AuditQuestion` and `AuditOption` are kept as the foundation with minor additions. `User` gains a `stakeholder_role` field collected at signup.

### Entity Relationship Overview

```
User ──────────────────────── AuditSession
  │  (1:many)                     │  (1:many)
  │                               │
  │                         AuditResponse ──── AuditQuestion ──── AuditOption
  │                               │                 │
  │                         WeaknessResult     BanditArmState
  │
StakeholderRoleEnum
```

---

### Model Definitions

#### `User` (extend existing)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | existing |
| email | EmailStr unique | existing |
| hashed_password | str | existing |
| is_active | bool | existing |
| is_superuser | bool | existing |
| full_name | str \| None | existing |
| created_at | datetime | existing |
| last_login_at | datetime \| None | existing |
| **stakeholder_role** | **StakeholderRoleEnum** | **new — collected at signup** |

**`StakeholderRoleEnum`**
```
software_developer | software_architect | project_manager
| qa_engineer | test_engineer | team_lead | aspice_assessor
```

---

#### `AuditQuestion` (refine existing)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | existing |
| question_code | str unique | e.g. `"SWE1-L1-Q01"` |
| process | ProcessEnum | SWE1–SWE6 |
| level | AspiceLevelEnum | L1 \| L2 \| L3 |
| base_practice_id | str | BP reference from ASPICE standard |
| question_text | str | existing |
| stakeholders | list[StakeholderRoleEnum] | JSON — roles that should see this question |
| recommendation_logic | str \| None | shown in results for high-weight answers |
| is_active | bool default=True | soft delete for question management |
| created_at | datetime | existing |

**`ProcessEnum`**
```
SWE1 | SWE2 | SWE3 | SWE4 | SWE5 | SWE6
```

---

#### `AuditOption` (keep existing — no changes)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| question_id | UUID FK→AuditQuestion CASCADE | |
| label | str | `"A"` through `"E"` |
| option_text | str | |
| weight | int 0–4 | 0 = no weakness, 4 = critical weakness |

---

#### `AuditSession` (new — replaces QuizAttempt)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | UUID FK→User CASCADE | |
| status | SessionStatusEnum | `in_progress \| completed \| abandoned` |
| questions_asked | list[UUID] JSON | ordered list of question IDs served so far |
| max_questions | int default=12 | configurable budget per session |
| started_at | datetime | |
| completed_at | datetime \| None | |

---

#### `AuditResponse` (new — one row per answered question)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| session_id | UUID FK→AuditSession CASCADE | |
| question_id | UUID FK→AuditQuestion | |
| option_id | UUID FK→AuditOption | selected answer |
| answered_at | datetime | |

---

#### `WeaknessResult` (new — computed at session completion)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| session_id | UUID FK→AuditSession unique | one result per session |
| scores | JSON | `{"SWE1": {"L1": 0.75, "L2": null, "L3": 0.2}, "SWE2": {...}, ...}` — `null` = not assessed |
| top_weaknesses | list[str] JSON | e.g. `["SWE3-L2", "SWE1-L1"]` — top 3 ranked gaps |
| computed_at | datetime | |

---

#### `BanditArmState` (new — CMAB per-question parameters)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| question_id | UUID FK→AuditQuestion unique | one row per question |
| A_matrix | JSON | LinUCB A matrix (23×23), serialized as nested list |
| b_vector | JSON | LinUCB b vector (23×1), serialized as list |
| pull_count | int default=0 | number of times this question was selected |
| total_reward | float default=0.0 | cumulative reward across all sessions |
| updated_at | datetime | |

---

## 4. CMAB Engine (Contextual Multi-Armed Bandit)

### Algorithm: LinUCB (Linear Upper Confidence Bound)

LinUCB is selected because:
- Well-understood update rule — interpretable for the thesis
- Handles contextual features naturally (user role, session state)
- Deterministic selection — reproducible experiments
- No training data required to start; improves online

### Context Vector `x` (23 dimensions)

Built fresh for each question-selection request:

```
x = [
  # User stakeholder role (one-hot, 7 dims)
  role_software_developer,
  role_software_architect,
  role_project_manager,
  role_qa_engineer,
  role_test_engineer,
  role_team_lead,
  role_aspice_assessor,

  # Session progress (1 dim)
  questions_answered / max_questions,     # 0.0 → 1.0

  # ASPICE processes already covered (6 dims, one per SWE process)
  swe1_covered, swe2_covered, swe3_covered,
  swe4_covered, swe5_covered, swe6_covered,   # 0 or 1

  # ASPICE levels already covered (3 dims)
  l1_covered, l2_covered, l3_covered,          # 0 or 1

  # Running weakness signal per process (6 dims)
  swe1_running_score, swe2_running_score, swe3_running_score,
  swe4_running_score, swe5_running_score, swe6_running_score  # 0.0 → 1.0
]
```

### Arm Eligibility Filter

Before running LinUCB selection, filter the question bank:

```python
eligible_arms = [
    q for q in all_active_questions
    if user.stakeholder_role in q.stakeholders       # role match
    and q.id not in session.questions_asked           # not already asked
]
```

### Arm Selection (UCB Score)

```
For each eligible arm a:
    θ_a  = A_a⁻¹ · b_a           # ridge regression estimate of reward
    ucb_a = θ_a ᵀ x + α · √(xᵀ · A_a⁻¹ · x)    # α = exploration parameter

selected_question = arm with highest ucb_a
```

`α` controls the exploration-exploitation tradeoff. Typical starting value: `α = 1.0`. This is a hyperparameter to tune and discuss in the thesis.

### Reward Signal (computed immediately after the user answers)

```
base_reward = option.weight / 4.0           # normalize 0–4 → 0.0–1.0

coverage_bonus = 0.2 if question.process not yet covered in session
                 else 0.0

reward = min(base_reward + coverage_bonus, 1.0)
```

The coverage bonus incentivizes the CMAB to explore all SWE processes rather than over-exploiting whichever process it has the most data on.

### Update Rule (after each answer)

```
A_a = A_a + x · xᵀ
b_a = b_a + reward · x
```

Both `A_a` and `b_a` are persisted to `BanditArmState` after each update. Global learning: the model improves across all users and sessions continuously.

### Initialization

Each new question starts with:
```
A_a = I   (23×23 identity matrix)
b_a = 0   (23-dimensional zero vector)
```

### Session Budget

- Default: `max_questions = 12` per session (configurable per audit by admin)
- Session ends when `len(questions_asked) == max_questions` **or** eligible questions are exhausted
- The budget is the core constraint the CMAB optimizes within

---

## 5. Weakness Classifier

Runs at session completion, consuming all `AuditResponse` rows for that session.

### Scoring Algorithm

```
For each (process, level) in {SWE1–SWE6} × {L1, L2, L3}:

    responses = all AuditResponse rows where
                    question.process == process
                    AND question.level == level

    if len(responses) == 0:
        score[process][level] = null        # not assessed this session

    else:
        score[process][level] = mean(option.weight for r in responses) / 4.0
        # → float 0.0 (fully compliant) to 1.0 (critical weakness)
```

### Classification Thresholds

| Score Range | Classification | Display Color |
|---|---|---|
| 0.00 – 0.25 | Compliant | Green |
| 0.25 – 0.50 | Minor Weakness | Yellow |
| 0.50 – 0.75 | Significant Gap | Orange |
| 0.75 – 1.00 | Critical Gap | Red |

### Top Weaknesses

The top 3 `(process, level)` pairs by score are stored in `WeaknessResult.top_weaknesses` (e.g., `["SWE3-L2", "SWE1-L1", "SWE5-L3"]`).

### Future Extension (thesis evolution chapter)

Once sufficient historical data accumulates (50+ completed sessions), the scoring function can be replaced with a trained supervised classifier:

- **Input:** encoded answer vector (one-hot per question × option)
- **Output:** weakness probability per `(process, level)` pair
- **Candidates:** logistic regression, gradient boosting (XGBoost), or a small neural network
- **Labels:** assessor-validated classifications from historical sessions

---

## 6. API Design

### What is Removed

The current generic `/quizzes` and `/statistics` endpoints are removed and replaced with ASPICE-specific routes below.

### Auth (existing, one addition)

```
POST  /api/v1/users/signup              — add stakeholder_role to signup payload
```

### Audit Sessions

```
POST  /api/v1/audit/sessions/               — start session, return first question
GET   /api/v1/audit/sessions/               — list current user's sessions (history)
GET   /api/v1/audit/sessions/{id}           — get session detail + questions asked
POST  /api/v1/audit/sessions/{id}/answer    — submit answer, return next question or completion
GET   /api/v1/audit/sessions/{id}/results   — get WeaknessResult for a completed session
```

### Question Bank (admin only)

```
GET   /api/v1/questions/            — list questions (filters: process, level, role, is_active)
POST  /api/v1/questions/            — create question with options
PATCH /api/v1/questions/{id}        — edit question or options
DELETE /api/v1/questions/{id}       — soft delete (sets is_active=False)
POST  /api/v1/questions/seed        — bulk seed from JSON payload
```

### Analytics (admin only)

```
GET   /api/v1/analytics/weaknesses  — aggregate weakness scores across all sessions,
                                      grouped by process and level
GET   /api/v1/analytics/users       — audit participation stats (sessions started/completed)
GET   /api/v1/analytics/bandit      — CMAB arm stats: pull counts, avg reward per question
```

### Core Answer Submission Flow

`POST /api/v1/audit/sessions/{id}/answer`

```
1. Validate session.status == in_progress
2. Validate question_id matches last question in session.questions_asked
3. Store AuditResponse (session_id, question_id, option_id, answered_at)
4. Compute reward from option.weight + coverage bonus
5. Update BanditArmState (A_matrix, b_vector) for that question
6. If len(questions_asked) < max_questions AND eligible questions remain:
     a. Build context vector x from current session state
     b. Run LinUCB arm selection over eligible questions
     c. Append selected question to session.questions_asked
     d. Return: { status: "in_progress", next_question: {...}, progress: {n/max} }
7. Else:
     a. Compute WeaknessResult from all AuditResponse rows
     b. Store WeaknessResult
     c. Set session.status = "completed", session.completed_at = now
     d. Return: { status: "completed", top_weaknesses: [...], session_id }
```

---

## 7. Frontend Design

### Page Changes

| Current Page | Status | Change |
|---|---|---|
| `signup.tsx` | Modify | Add stakeholder role dropdown |
| `admin-quizzes.tsx` | Replace | Question Bank Manager (process/level/role filters) |
| `quizzes/index.tsx` | Replace | Audits list — show sessions, start button |
| `quizzes/$quizId` | Replace | Audit Session page (one question at a time) |
| `quizzes/$quizId/result` | Replace | Weakness Results page |
| `history.tsx` | Modify | Show past AuditSessions with weakness scores |
| `dashboard.tsx` | Modify | Admin aggregate weakness heatmap |

### Audit Session Page Flow

```
User clicks "Start Audit"
    → POST /api/v1/audit/sessions/
    → Display first question with options A–E
    → Show progress bar: "Question 1 of 12"

User selects option → clicks "Submit"
    → POST /api/v1/audit/sessions/{id}/answer
    → If status == "in_progress": display next question, update progress bar
    → If status == "completed": navigate to results page

Results Page:
    → GET /api/v1/audit/sessions/{id}/results
    → Display weakness radar chart + color-coded heatmap table
    → List top weaknesses with recommendation text
```

### Signup Role Selection

```
Name _______________
Email ______________
Password ___________

Your Role in the Project:
  ○ Software Developer
  ○ Software Architect
  ○ Project Manager
  ○ QA Engineer
  ○ Test Engineer
  ○ Team Lead
  ○ ASPICE Assessor

[ Create Account ]
```

### Results Page Visualizations

**1. Radar Chart**
- 6 axes: SWE.1 through SWE.6
- Each axis value = mean score across all levels assessed for that process
- Shows overall process health at a glance

**2. Heatmap Table**

| Process | L1 | L2 | L3 |
|---|---|---|---|
| SWE.1 | 🟡 0.35 | 🟢 0.10 | — |
| SWE.2 | 🟠 0.60 | — | — |
| SWE.3 | 🔴 0.82 | 🟡 0.40 | 🟢 0.15 |
| SWE.4 | 🟢 0.20 | — | — |
| SWE.5 | — | 🟠 0.55 | — |
| SWE.6 | 🟢 0.10 | 🟢 0.05 | — |

`—` = not assessed in this session

**3. Top Weaknesses + Recommendations**
- Ranked list of (process, level) pairs with highest scores
- Recommendation text pulled from `AuditQuestion.recommendation_logic` for high-weight answers in that session

### Admin Dashboard

- Aggregate heatmap across all completed sessions
- Trend chart: weakness scores over time (by week)
- CMAB arm stats: which questions are selected most, average reward per question
- User participation: sessions started/completed by role

---

## 8. Key Design Decisions

### Why LinUCB over Thompson Sampling?

LinUCB produces a deterministic selection given the same context and model state, making it reproducible for thesis experiments. It has an interpretable update rule and the exploration parameter `α` is a single, explainable hyperparameter. Thompson Sampling introduces stochastic sampling that is harder to analyze and explain.

### Why not serve all questions in one fixed quiz?

The CMAB budget (12 questions) models the real-world constraint that stakeholders have limited time. The algorithm's contribution is to extract maximum diagnostic signal within that budget by learning which questions are most informative for a given user role and session context. A fixed quiz cannot adapt.

### Why immediate reward rather than deferred expert validation?

Reward is computed from `option.weight` immediately after answering. This makes the system self-contained without requiring an ASPICE assessor to label every session. The thesis discusses deferred/expert-label reward as a future work direction that would increase accuracy once a labelled dataset exists.

### Why keep `AuditQuestion` separate from `BanditArmState`?

Question content (text, process, level, options) is managed by admins and changes infrequently. CMAB selection policy (`A_matrix`, `b_vector`) updates continuously after every user answer. Separating them means admin edits to question text do not interfere with the learned bandit model.

### Why weighted scoring for the classifier rather than a trained ML model?

The weighted scoring approach is auditable, requires no training data, and works from day one. It is the right MVP. The thesis positions a trained supervised classifier as the natural next step once 50+ labelled sessions exist — this is an explicit contribution boundary.

### Weakness score normalization

Option weights (0–4) are normalized to 0.0–1.0 by dividing by 4. This makes scores comparable across questions regardless of the number of options, and maps cleanly to the four-level classification thresholds.

---

## 9. Python Package Layout

```
backend/app/
├── services/
│   ├── __init__.py
│   ├── audit_service.py          # session start/answer/complete workflow
│   ├── cmab_engine.py            # LinUCB: context builder, arm select, update
│   └── weakness_classifier.py   # weighted scoring + thresholds + top_weaknesses
├── api/
│   ├── main.py                   # router registration
│   ├── deps.py                   # auth + DB session dependencies
│   └── routes/
│       ├── audit.py              # /audit/sessions/* endpoints
│       ├── questions.py          # /questions/* endpoints (admin)
│       ├── analytics.py          # /analytics/* endpoints (admin)
│       ├── users.py              # /users/* endpoints
│       └── login.py              # /login/* endpoints
├── models.py                     # SQLModel DB models + Pydantic schemas
├── crud.py                       # DB helper functions
└── seed_questions.py             # one-time question bank seeding script
```

### Service responsibilities

**`audit_service.py`**
- `start_session(user, db) → (AuditSession, AuditQuestionPublic)` — creates session, calls CMAB for first question
- `submit_answer(session_id, question_id, option_id, db) → AnswerResult` — stores response, updates CMAB, returns next question or triggers completion
- `_complete_session(session, db) → WeaknessResult` — calls classifier, stores result, marks session done

**`cmab_engine.py`**
- `build_context(session, user, db) → np.ndarray` — builds 23-dim context vector
- `select_question(context, eligible_questions, db) → AuditQuestion` — LinUCB UCB arm selection
- `update_arm(question_id, context, reward, db)` — updates A/b matrices, persists to DB
- `compute_reward(option, question, session, db) → float` — base reward + coverage bonus, clamped [0, 1]

**`weakness_classifier.py`**
- `compute_scores(session_id, db) → dict` — returns `{process: {level: score | null}}` for all 18 cells
- `get_top_weaknesses(scores, n=3) → list[str]` — returns top N `"SWEX-LY"` keys by score

---

## 10. Implementation Status

All phases implemented. The migration path described in the original design has been fully executed:

| Step | Status |
|---|---|
| Add `stakeholder_role` to `user` (Alembic) | ✅ Done |
| Create `auditsession`, `auditresponse`, `weaknessresult`, `banditarmstate` tables | ✅ Done |
| Add `base_practice_id` and `is_active` to `auditquestion` | ✅ Done |
| Drop `quiz`, `question`, `quizattempt` tables | ✅ Done |
| Implement services package + API routes | ✅ Done |
| Update all frontend pages | ✅ Done |
| Seed 42 questions across SWE.1–SWE.6 | ✅ Done |

---

*Architecture version 1.0 — June 2026*
