# ASPICE Audit — Implementation To-Do List

Tasks are ordered by dependency. Complete each phase before starting the next.  
Reference: [Architecture.md](Architecture.md)

---

## Phase 1 — Database Models

> All API and service work depends on the schema being correct first.

- [ ] **1.1** Add `StakeholderRoleEnum` to `models.py`
  - Values: `software_developer | software_architect | project_manager | qa_engineer | test_engineer | team_lead | aspice_assessor`

- [ ] **1.2** Add `stakeholder_role: StakeholderRoleEnum` field to `User` model

- [ ] **1.3** Add `ProcessEnum` to `models.py`
  - Values: `SWE1 | SWE2 | SWE3 | SWE4 | SWE5 | SWE6`

- [ ] **1.4** Refine `AuditQuestion` model
  - Add `base_practice_id: str` (BP reference from ASPICE standard)
  - Change `process` field type from `str` to `ProcessEnum`
  - Change `stakeholders` field type from `list[str]` to `list[StakeholderRoleEnum]`
  - Add `is_active: bool = True` (soft delete support)
  - Remove unused fields: `criteria`, `identifies` (consolidate into `question_text`)

- [ ] **1.5** Verify `AuditOption` model is correct (weight 0–4, label A–E) — no changes needed if so

- [ ] **1.6** Create `AuditSession` model
  - Fields: `id`, `user_id FK→User`, `status: SessionStatusEnum`, `questions_asked: list[UUID] JSON`, `max_questions: int = 12`, `started_at`, `completed_at`
  - Add `SessionStatusEnum`: `in_progress | completed | abandoned`

- [ ] **1.7** Create `AuditResponse` model
  - Fields: `id`, `session_id FK→AuditSession CASCADE`, `question_id FK→AuditQuestion`, `option_id FK→AuditOption`, `answered_at`

- [ ] **1.8** Create `WeaknessResult` model
  - Fields: `id`, `session_id FK→AuditSession unique`, `scores: JSON`, `top_weaknesses: list[str] JSON`, `computed_at`
  - `scores` shape: `{"SWE1": {"L1": 0.75, "L2": null}, ...}`

- [ ] **1.9** Create `BanditArmState` model
  - Fields: `id`, `question_id FK→AuditQuestion unique`, `A_matrix: JSON`, `b_vector: JSON`, `pull_count: int = 0`, `total_reward: float = 0.0`, `updated_at`

- [ ] **1.10** Add public response schemas (Pydantic) for all new models
  - `AuditSessionPublic`, `AuditResponsePublic`, `WeaknessResultPublic`, `BanditArmStatePublic`

---

## Phase 2 — Database Migrations

> Run after all model definitions are final.

- [ ] **2.1** Generate Alembic migration: add `stakeholder_role` to `user` table
  - Set default value `software_developer` for existing rows before applying `NOT NULL`

- [ ] **2.2** Generate Alembic migration: add `base_practice_id` and `is_active` to `auditquestion` table

- [ ] **2.3** Generate Alembic migration: create `auditsession`, `auditresponse`, `weaknessresult`, `banditarmstate` tables

- [ ] **2.4** Generate Alembic migration: drop `quiz`, `question`, `quizattempt` tables
  - Verify no data needs preserving before running

- [ ] **2.5** Run all migrations in local Docker environment and verify with Adminer

---

## Phase 3 — CMAB Engine

> Core ML component. Must be implemented and unit-tested before building the audit service.

- [ ] **3.1** Create `backend/app/services/` package (add `__init__.py`)

- [ ] **3.2** Implement `backend/app/services/cmab_engine.py`

  - [ ] **3.2.1** Implement `build_context(session: AuditSession, user: User) -> np.ndarray`
    - One-hot encode `user.stakeholder_role` (7 dims)
    - Compute session progress: `len(questions_asked) / max_questions` (1 dim)
    - Compute per-process coverage flags from `questions_asked` (6 dims)
    - Compute per-level coverage flags from `questions_asked` (3 dims)
    - Compute running mean weakness score per process from answered responses (6 dims)
    - Return 23-dim numpy array

  - [ ] **3.2.2** Implement `select_question(context: np.ndarray, eligible_questions: list[AuditQuestion], db: Session) -> AuditQuestion`
    - Load `BanditArmState` for each eligible question (create with identity A, zero b if not exists)
    - Compute UCB score: `θᵀx + α · √(xᵀ · A⁻¹ · x)` where `α = 1.0`
    - Return question with highest UCB score

  - [ ] **3.2.3** Implement `compute_reward(option: AuditOption, session: AuditSession) -> float`
    - Base reward: `option.weight / 4.0`
    - Coverage bonus: `+0.2` if `option.question.process` not yet in `session.questions_asked`
    - Clamp to `[0.0, 1.0]`

  - [ ] **3.2.4** Implement `update_arm(question_id: UUID, context: np.ndarray, reward: float, db: Session)`
    - Load `BanditArmState` for question
    - Update: `A = A + x · xᵀ`, `b = b + reward · x`
    - Increment `pull_count`, add to `total_reward`
    - Persist updated state to DB

- [ ] **3.3** Write unit tests for `cmab_engine.py`
  - Test `build_context` produces correct shape and value ranges
  - Test `select_question` always returns a question from the eligible list
  - Test `update_arm` correctly modifies A and b matrices
  - Test `compute_reward` clamps to [0.0, 1.0]

---

## Phase 4 — Weakness Classifier

- [ ] **4.1** Implement `backend/app/services/weakness_classifier.py`

  - [ ] **4.1.1** Implement `compute_scores(session_id: UUID, db: Session) -> dict`
    - For each `(process, level)` pair in `{SWE1–SWE6} × {L1, L2, L3}`:
      - Fetch `AuditResponse` rows matching that process and level
      - If empty → score = `null`
      - Else → score = `mean(option.weight) / 4.0`
    - Return nested dict `{process: {level: score | null}}`

  - [ ] **4.1.2** Implement `classify(score: float | None) -> str`
    - `null` → `"not_assessed"`
    - `0.00–0.25` → `"compliant"`
    - `0.25–0.50` → `"minor_weakness"`
    - `0.50–0.75` → `"significant_gap"`
    - `0.75–1.00` → `"critical_gap"`

  - [ ] **4.1.3** Implement `get_top_weaknesses(scores: dict, n: int = 3) -> list[str]`
    - Flatten scores to list of `(process_level_key, score)` tuples (excluding nulls)
    - Sort descending by score
    - Return top `n` keys, e.g. `["SWE3-L2", "SWE1-L1"]`

- [ ] **4.2** Write unit tests for `weakness_classifier.py`
  - Test all four classification thresholds
  - Test `null` handling when no questions answered for a (process, level)
  - Test `get_top_weaknesses` ordering

---

## Phase 5 — Audit Service

- [ ] **5.1** Implement `backend/app/services/audit_service.py`

  - [ ] **5.1.1** Implement `start_session(user: User, db: Session) -> tuple[AuditSession, AuditQuestion]`
    - Create `AuditSession` with `status=in_progress`
    - Build initial context vector (empty session)
    - Get eligible questions for user role
    - Call `cmab_engine.select_question` for first question
    - Append question ID to `session.questions_asked`
    - Return session and first question with its options

  - [ ] **5.1.2** Implement `submit_answer(session_id: UUID, question_id: UUID, option_id: UUID, db: Session) -> AnswerResult`
    - Validate session is `in_progress`
    - Validate `question_id` matches last entry in `session.questions_asked`
    - Create `AuditResponse` record
    - Compute reward via `cmab_engine.compute_reward`
    - Call `cmab_engine.update_arm`
    - If budget remaining and eligible questions exist:
      - Build updated context
      - Select next question via CMAB
      - Append to `session.questions_asked`
      - Return `{ status: "in_progress", next_question, progress }`
    - Else:
      - Call `complete_session`
      - Return `{ status: "completed", top_weaknesses, session_id }`

  - [ ] **5.1.3** Implement `complete_session(session: AuditSession, db: Session) -> WeaknessResult`
    - Call `weakness_classifier.compute_scores`
    - Call `weakness_classifier.get_top_weaknesses`
    - Create and store `WeaknessResult`
    - Set `session.status = completed`, `session.completed_at = now()`
    - Return `WeaknessResult`

---

## Phase 6 — Backend API Routes

- [ ] **6.1** Create `backend/app/api/routes/audit.py`

  - [ ] **6.1.1** `POST /audit/sessions/` — Start new audit session
    - Auth required (any role)
    - Calls `audit_service.start_session`
    - Returns: `AuditSessionPublic` + first `AuditQuestionPublic`

  - [ ] **6.1.2** `GET /audit/sessions/` — List current user's sessions
    - Auth required
    - Returns: paginated list of `AuditSessionPublic` ordered by `started_at` desc

  - [ ] **6.1.3** `GET /audit/sessions/{id}` — Get session detail
    - Auth required (own session or admin)
    - Returns: `AuditSessionPublic` with `questions_asked` list

  - [ ] **6.1.4** `POST /audit/sessions/{id}/answer` — Submit answer
    - Auth required (own session only)
    - Body: `{ question_id: UUID, option_id: UUID }`
    - Calls `audit_service.submit_answer`
    - Returns: next question or completion signal

  - [ ] **6.1.5** `GET /audit/sessions/{id}/results` — Get weakness results
    - Auth required (own session or admin)
    - Returns: `WeaknessResultPublic`

- [ ] **6.2** Create `backend/app/api/routes/questions.py`

  - [ ] **6.2.1** `GET /questions/` — List questions (admin only)
    - Query params: `process`, `level`, `stakeholder_role`, `is_active`
    - Returns: paginated list of `AuditQuestionPublic` with options

  - [ ] **6.2.2** `POST /questions/` — Create question with options (admin only)
    - Body: question fields + list of option objects
    - Also initializes `BanditArmState` for new question

  - [ ] **6.2.3** `PATCH /questions/{id}` — Update question or its options (admin only)

  - [ ] **6.2.4** `DELETE /questions/{id}` — Soft delete (admin only)
    - Sets `is_active = False`, does not remove `BanditArmState`

  - [ ] **6.2.5** `POST /questions/seed` — Bulk seed from JSON payload (admin only)
    - Accepts list of question objects
    - Idempotent: skips questions where `question_code` already exists

- [ ] **6.3** Create `backend/app/api/routes/analytics.py`

  - [ ] **6.3.1** `GET /analytics/weaknesses` — Aggregate weakness heatmap (admin only)
    - Averages `WeaknessResult.scores` across all completed sessions
    - Returns: `{process: {level: avg_score}}` for all 18 (process, level) pairs

  - [ ] **6.3.2** `GET /analytics/users` — User participation stats (admin only)
    - Returns: sessions started/completed per role, total users per role

  - [ ] **6.3.3** `GET /analytics/bandit` — CMAB arm performance (admin only)
    - Returns: per-question `pull_count`, `avg_reward`, `question_code`, `process`, `level`
    - Useful for thesis analysis and debugging

- [ ] **6.4** Register new routes in `backend/app/api/main.py`
  - Add `audit`, `questions`, `analytics` routers
  - Remove `quizzes` and `statistics` routers

- [ ] **6.5** Remove `backend/app/api/routes/quizzes.py` and `statistics.py`

- [ ] **6.6** Update `backend/app/crud.py`
  - Remove quiz-related CRUD functions
  - Add CRUD helpers for `AuditSession`, `AuditResponse`, `WeaknessResult`, `BanditArmState`

---

## Phase 7 — Question Bank Seed Data

> The application cannot be used without questions. Seed data must be ready before frontend testing.

- [ ] **7.1** Design question bank JSON structure
  - One file per process: `questions_swe1.json` through `questions_swe6.json`
  - Each question includes: `question_code`, `process`, `level`, `base_practice_id`, `question_text`, `stakeholders`, `recommendation_logic`, `options[]`

- [ ] **7.2** Write seed questions for **SWE.1** (Software Requirements Analysis)
  - Minimum 5 questions per level (L1, L2, L3) = 15 questions
  - Cover all relevant stakeholder roles

- [ ] **7.3** Write seed questions for **SWE.2** (Software Architectural Design)
  - Minimum 5 questions per level = 15 questions

- [ ] **7.4** Write seed questions for **SWE.3** (Software Detailed Design & Unit Construction)
  - Minimum 5 questions per level = 15 questions

- [ ] **7.5** Write seed questions for **SWE.4** (Software Unit Verification)
  - Minimum 5 questions per level = 15 questions

- [ ] **7.6** Write seed questions for **SWE.5** (Software Integration & Integration Test)
  - Minimum 5 questions per level = 15 questions

- [ ] **7.7** Write seed questions for **SWE.6** (Software Qualification Test)
  - Minimum 5 questions per level = 15 questions

- [ ] **7.8** Create `backend/app/seed_aspice_questions.py` script
  - Reads all six JSON files and calls `POST /questions/seed`
  - Run via `docker compose exec backend python app/seed_aspice_questions.py`

---

## Phase 8 — Frontend: Auth & Signup

- [ ] **8.1** Update `frontend/src/routes/signup.tsx`
  - Add stakeholder role selection after the password field (radio buttons or dropdown)
  - Map display names to `StakeholderRoleEnum` values
  - Include `stakeholder_role` in the signup API request body

- [ ] **8.2** Update API client
  - Regenerate client from updated OpenAPI schema: `npm run generate-client`
  - Verify `UserRegister` schema includes `stakeholder_role`

---

## Phase 9 — Frontend: Audit Session Flow

- [ ] **9.1** Replace `frontend/src/routes/_layout/quizzes/index.tsx` with Audits list page
  - Fetch user's sessions from `GET /audit/sessions/`
  - Display: status badge, started date, top weaknesses preview for completed sessions
  - Prominent "Start New Audit" button → calls `POST /audit/sessions/`

- [ ] **9.2** Create `frontend/src/routes/_layout/audit/$sessionId/index.tsx` — Audit Session page
  - On load: fetch current session state; if `in_progress`, display last unanswered question
  - Display question text and options A–E as radio buttons or cards
  - Show progress bar: "Question N of 12"
  - On submit: call `POST /audit/sessions/{id}/answer`
  - If response `status == "in_progress"`: render next question (no page reload)
  - If response `status == "completed"`: navigate to results page

- [ ] **9.3** Create `frontend/src/routes/_layout/audit/$sessionId/results.tsx` — Results page
  - Fetch `GET /audit/sessions/{id}/results`

  - [ ] **9.3.1** Implement radar chart (SWE.1–SWE.6 axes, one value per process)
    - Use `recharts` or `chart.js` (whichever is already in `package.json`)

  - [ ] **9.3.2** Implement heatmap table (rows = processes, columns = L1/L2/L3)
    - Color-code cells: green / yellow / orange / red based on score thresholds
    - Show `—` for null (not assessed)

  - [ ] **9.3.3** Implement top weaknesses list
    - Show top 3 gaps with process name, level, score, and recommendation text

- [ ] **9.4** Update sidebar navigation
  - Rename "Quizzes" entry to "Audits"
  - Update route links to new audit paths

---

## Phase 10 — Frontend: History Page

- [ ] **10.1** Update `frontend/src/routes/_layout/history.tsx`
  - Fetch sessions from `GET /audit/sessions/`
  - Table columns: Date, Status, Questions Answered, Top Weakness, Actions
  - "View Results" link for completed sessions → navigates to results page
  - "Continue" link for in-progress sessions → navigates to audit session page

---

## Phase 11 — Frontend: Admin Pages

- [ ] **11.1** Replace `frontend/src/routes/_layout/admin-quizzes.tsx` with Question Bank Manager
  - Table: question code, process, level, stakeholders, is_active, actions
  - Filter bar: by process, level, stakeholder role, active/inactive
  - "Add Question" button → opens modal/drawer with form (question + options)
  - "Edit" and "Deactivate" actions per row

- [ ] **11.2** Update `frontend/src/routes/_layout/dashboard.tsx` — Admin Analytics Dashboard
  - Aggregate weakness heatmap from `GET /analytics/weaknesses`
  - User participation stats from `GET /analytics/users`
  - CMAB arm performance table from `GET /analytics/bandit`
  - Remove old quiz statistics widgets

---

## Phase 12 — Integration & Testing

- [ ] **12.1** Run full Docker stack locally and verify end-to-end flow
  - Signup with each stakeholder role
  - Start audit, answer all 12 questions, reach results page
  - Verify weakness scores and chart render correctly

- [ ] **12.2** Write API integration tests for audit session flow
  - Test: start session → submit answers → complete → get results
  - Test: cannot submit answer to wrong question
  - Test: session marked completed after max_questions reached

- [ ] **12.3** Write API integration tests for question bank endpoints
  - Test: create question initializes `BanditArmState`
  - Test: soft delete sets `is_active=False`
  - Test: seed endpoint is idempotent

- [ ] **12.4** Verify CMAB learns across sessions
  - Run 5+ simulated sessions with scripted answers
  - Check that `pull_count` and `total_reward` in `BanditArmState` update correctly
  - Check that question selection varies based on user role

- [ ] **12.5** Update Playwright E2E tests
  - Remove quiz-related tests
  - Add audit session flow test (signup → start audit → answer questions → view results)

---

## Phase 13 — Cleanup & Documentation

- [ ] **13.1** Remove unused boilerplate
  - Delete `backend/app/api/routes/items.py` if not used
  - Delete corresponding frontend items page if not needed
  - Remove `Quiz`, `Question`, `QuizAttempt` from `models.py` after migration confirmed working

- [ ] **13.2** Update `backend/README.md` with new API routes and setup instructions

- [ ] **13.3** Update root `README.md` with project overview matching thesis scope

- [ ] **13.4** Update `Architecture.md` if any design decisions change during implementation

---

## Summary

| Phase | Area | Tasks |
|---|---|---|
| 1–2 | Database Models & Migrations | 15 tasks |
| 3–4 | CMAB Engine & Weakness Classifier | 12 tasks |
| 5 | Audit Service | 3 tasks |
| 6 | Backend API Routes | 18 tasks |
| 7 | Question Bank Seed Data | 8 tasks |
| 8 | Frontend Auth | 2 tasks |
| 9 | Frontend Audit Session Flow | 7 tasks |
| 10 | Frontend History | 1 task |
| 11 | Frontend Admin Pages | 2 tasks |
| 12 | Integration & Testing | 5 tasks |
| 13 | Cleanup & Documentation | 4 tasks |
| **Total** | | **77 tasks** |

---

*To-do list version 1.0 — June 2026*
