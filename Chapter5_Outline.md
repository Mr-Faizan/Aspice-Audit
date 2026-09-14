# Chapter 5 Outline — Implementation (10–15 pages)

> Planning scaffold only — not thesis prose. Bullet points per heading (matching the stub
> headers already in `writing/Template.tex`), plus which figure/table belongs where, sourced
> from `Implementation.md`, `Architecture.md`, and `writing/documents/visual_assets_checklist.md`.

---

## ⚠️ Pending functionality changes — read before writing prose

Two changes are planned but **not yet in the code**. Everything below is outlined against the
*current* implementation (fixed `max_questions=12`, per-question pre-tagged `level`). Each
subsection affected is marked **[PENDING-A]** or **[PENDING-B]** below.

- **[PENDING-A] Adaptive session length.** `max_questions` becomes a ceiling, not a target.
  Session ends early if no more weaknesses turn up; digs deeper (asks more related questions)
  into a process if a weakness is found. Already reflected in the Chapter 4 text
  (`Session Budget` subsection). Affects: CMAB context vector's progress dimension, the audit
  session service's stopping logic, the "Question X of 12" screenshot/UI text, and one
  implementation-challenges bullet.
- **[PENDING-B] System-derived capability level.** Instead of each question being pre-tagged
  with a fixed `level` (L1/L2/L3) by the question-bank author, the level is determined by the
  system from the pattern of answers (closer to how ISO 33020 actually derives a capability
  level from process-attribute ratings, rather than a static per-question label). Affects: the
  question bank's data model framing, the weakness classifier's scoring logic, and the results
  heatmap's meaning.

Don't write final prose for the flagged bullets yet — write the current-implementation version,
and revisit once the code changes land. Where a change is likely to be substantial, I've noted
it explicitly rather than guessing the new mechanism.

---

## Section: Development Environment and Tooling

### Containerized Development Environment (Docker Compose Watch)
- What to write: why Docker Compose was chosen for local dev, what `watch` mode gives you
  (live rebuild/sync on file change instead of full container rebuild), which services run
  (frontend, backend, db, adminer).
- Figure: **Infrastructure diagram** (Docker Compose topology) — checklist item F, shared
  Ch.4.2/Ch.5.5; I'd place the actual figure in §Deployment/"Docker Compose Services" below and
  just `\ref` it here to avoid duplicating the same diagram twice.
- Optional figure: terminal screenshot of `docker compose watch` running (checklist E,
  optional) — nice but skippable.
- Table: not needed here.

### Backend Development Stack (FastAPI, SQLModel, uv, Alembic)
- What to write: one paragraph per tool — FastAPI (async, typed, auto-docs), SQLModel (single
  model class serves as both ORM table and Pydantic schema), `uv` (fast Python package/dep
  manager), Alembic (versioned schema migrations) — why each was chosen over an alternative.
- Figure: share the **Technologies Used diagram** with the next subsection (see below).
- Table: good candidate — a small "Technology choices" table (Layer | Technology | Why),
  covering both backend and frontend stacks in one table so it isn't split awkwardly across
  two subsections.

### Frontend Development Stack (React, TypeScript, Vite, TanStack Router)
- What to write: React+TS for type safety across components, Vite for fast dev server/HMR,
  TanStack Router for type-safe file-based routing (ties into the routing table later in
  Frontend Implementation).
- Figure: **Technologies Used diagram** — checklist D, Figure 6, explicitly assigned to
  Ch.5.1. Redraw with your *actual* stack (FastAPI, PostgreSQL/SQLModel, React+TS+Vite+TanStack,
  JWT, Docker Compose), not the generic pitched one from the concept presentation.
- Table: the shared tech-choices table from the previous subsection.

---

## Section: Backend Implementation

### Backend Project Structure
- What to write: walk the package layout from `Architecture.md` §9 — `services/`, `api/`
  (with `deps.py`, `routes/`), `models.py`, `crud.py`, `seed_questions.py`. Explain the
  layering rationale (routes stay thin, business logic lives in services, per Ch.4's API
  Responsibilities subsection).
- Figure: not needed — present the tree as a `verbatim`/code listing, not an image.
- Table: not needed.

### Data Models and Database Migrations
- What to write: SQLModel definitions for the extended `User` and the new
  `AuditQuestion`/`AuditOption`/`AuditSession`/`AuditResponse`/`WeaknessResult`/`BanditArmState`
  tables; note what Alembic migration steps were needed (add column, create tables, drop old
  `quiz`/`question`/`quizattempt` tables).
- Figure: don't recreate the ERD — it's already `fig:erd` (`Arch_4.png`) in Chapter 4; just
  `\ref` it.
- Table: good candidate — turn `Architecture.md` §10's migration-status table into a real
  LaTeX table (Step | Status), since it's already in checklist form and reads well as evidence
  of what was actually done.
- **[PENDING-B]**: once system-derived levels land, the `AuditQuestion.level` field's role
  changes (author-assigned vs. system-inferred) — flag as a footnote for revision, don't
  redesign the table now.

### Audit Session Service (`audit_service.py`)
- What to write: `start_session`, `submit_answer`, `_complete_session` — what each does, how
  they call into the CMAB engine and classifier, transaction boundaries around answer
  submission.
- Figure: don't recreate the sequence diagram — it's already `fig:arch-answer-sequence`
  (`Arch_6_Sequence_diagram.png`) in Chapter 4; `\ref` it, maybe zoom into one step with a short
  code snippet instead.
- Table: not needed.
- **[PENDING-A]**: this is where the fixed "steps 3–4 repeat for up to 12 questions" stopping
  logic currently lives (`Implementation.md` §4, step 5) — this function's control flow is what
  actually changes for adaptive stopping. Write the *current* logic; note inline that this is
  the first place to touch when the change lands.

### CMAB Engine Implementation (`cmab_engine.py`)
- What to write: `build_context`, `select_question`, `update_arm`, `compute_reward` — map each
  function to the math already covered in Chapter 4 (context vector, UCB score, reward,
  update rule), but now at the code level (numpy arrays, JSON (de)serialization of `A`/`b` for
  `BanditArmState` storage).
- Figure: **Context vector diagram** — checklist F, a labeled bar/table of the 23 dimensions.
  Checklist originally assigned this to Ch.4.5.2, but Chapter 4 ended up describing the vector
  in prose only, no figure — your call whether to add it there instead, or use it here where
  the actual array construction is discussed. I'd lean toward here, since it's a code-level
  visual, but flagging so you can decide.
- Table: strong alternative to the diagram — `Implementation.md` §2.3 already has the 23
  dimensions as a markdown table (Dimensions | Content | How computed); converting that
  directly to a LaTeX table might be clearer than a diagram and is less work.
- **[PENDING-A]**: dimension 7 ("session progress", `questions_asked / max_questions`) needs
  re-describing once `max_questions` becomes a ceiling rather than a target — the ratio still
  works, but the framing sentence needs a tweak.

### Weakness Classifier Implementation (`weakness_classifier.py`)
- What to write: `compute_scores`, `get_top_weaknesses` — map to the scoring algorithm and
  4-band thresholds already in Chapter 4 (don't repeat the thresholds table, just `\ref` it);
  focus on the code-level detail (grouping responses by process×level, handling `null` for
  uncovered cells).
- Figure: don't recreate — `fig:question-to-result` (`Arch_5.png`) already covers this in
  Chapter 4.
- Table: not needed (already covered).
- **[PENDING-B]**: this is the section most affected by system-derived levels — the whole
  "group responses by the question's pre-tagged level" approach is what's being replaced.
  Write the current implementation faithfully; this subsection will need the heaviest rewrite
  once the new logic is designed, so keep the current prose modular/short rather than deeply
  intertwined with the rest of the section.

### API Routes and Dependency Injection
- What to write: route grouping (`/audit`, `/questions`, `/analytics`, `/users`, `/login`),
  `deps.py` for auth + DB session injection, `main.py` router registration.
- Figure: optional Swagger/OpenAPI docs screenshot (checklist E, optional, explicitly called
  out as "nice for Ch.5 API implementation").
- Table: good candidate — Chapter 4 already has a table for the three *session* endpoints;
  add a parallel table here for the *admin* endpoints (question bank: list/create/patch/
  delete/seed; analytics: `/weaknesses`, `/users`, `/bandit`), since those aren't tabulated
  anywhere yet.

### Authentication and Authorization
- What to write: JWT issuance/validation flow at the code level, `is_superuser` dependency
  check, signup payload extension with `stakeholder_role`.
- Figure: Signup page screenshot (checklist E) fits well here, or defer it to Frontend
  Implementation's "Authentication and User Management" subsection — pick one location, don't
  duplicate.
- Table: not needed (conceptually already covered in Chapter 4).

---

## Section: Question Bank Implementation

### Question Bank Data Preparation
- What to write: how the 60 questions / 300 options were authored from the PAM base
  practices, coverage rationale (6 processes × 10 questions, spread across each process's base
  practices so no single practice is over- or under-represented).
- Figure: not needed.
- Table: good candidate — a summary count table (60 questions, 300 options, 6 processes,
  10 questions/process, 5 options/question).
- **[PENDING-B]**: this subsection currently frames level as an authoring-time decision
  ("each question belongs to exactly one process and one level" — `Implementation.md` §3.1).
  That's the exact framing the pending change replaces. Write it as current state; this is the
  second subsection (after the classifier) that will need real rework later.

### Seed Script and Idempotent Seeding
- What to write: `seed_questions.py` — bulk-load approach, idempotency mechanism (e.g.
  upsert-by-`question_code` so re-running the seed script doesn't duplicate rows), how/when
  it's invoked.
- Figure/table: not needed; a short code snippet is enough.

### Traceability and Stakeholder Role Fields
- What to write: `base_practice_id` and how it satisfies NFR2 (already established in
  Chapter 4 — just tie back to it here at the implementation level), `stakeholders` list field
  and how the eligibility filter reads it.
- Figure/table: not needed — reference the existing example-question table from Chapter 4
  rather than duplicating it.

---

## Section: Frontend Implementation

### Frontend Project Structure and Routing
- What to write: TanStack Router's file-based routing, the page list mapped from
  `Architecture.md` §7 (signup, login, audits list, session page, results page, history, admin
  dashboard).
- Figure: not needed (or an optional routing-tree diagram if it aids clarity).
- Table: good candidate — adapt `Architecture.md` §7's "Page Changes" table (Current Page |
  Status | Change) into a real LaTeX table; it already reads well as-is.

### Authentication and User Management
- What to write: signup form (role dropdown), login form, token storage/handling, protected
  route behavior.
- Figure: Signup page screenshot, Login page screenshot (both checklist E) — put both here if
  you didn't already place Signup in the backend Auth subsection.
- Table: not needed.

### Assessment Session and Question Interaction (Screenshots)
- What to write: the audit session page flow end to end (start button → first question →
  one-question-at-a-time with progress bar → submit → next question or redirect to results),
  matching `Architecture.md` §7's "Audit Session Page Flow".
- Figure: Audits/dashboard list page screenshot; audit session screen mid-flow screenshot,
  both checklist E.
- Table: not needed.
- **[PENDING-A]**: the mid-flow screenshot currently shows "Question X of 12" — if you capture
  this screenshot before the adaptive-length change ships, note in the caption that the fixed
  denominator reflects the implementation at time of writing; otherwise wait to capture until
  after the change, or reword the UI copy first.

### Results Dashboard and Visualization (Screenshots)
- What to write: radar chart, heatmap table, top-3-weaknesses-with-recommendations — what
  charting approach/library renders these (confirm from the actual frontend code before
  writing final prose; not specified in `Implementation.md`).
- Figure: three screenshots from checklist E (radar chart, heatmap table, top-3 list).
- Table: not needed — the heatmap itself is a screenshot, not a LaTeX table.
- **[PENDING-B]**: once levels are system-derived, what the heatmap's L1/L2/L3 columns actually
  represent changes (from "score for questions pre-tagged at that level" to "system-inferred
  standing"). Flag in a footnote; don't rewrite the visualization description yet.

### Administration and Question Bank Management (Screenshots)
- What to write: Question Bank Manager (list/filter/edit questions and options), Analytics
  Dashboard (aggregate heatmap, CMAB arm stats, participation stats).
- Figure: five screenshots from checklist E — question bank list view, single-question
  edit/detail view, aggregate weakness heatmap, CMAB arm performance table, user participation
  stats.
- Table: not needed (screenshots cover it), unless you want to show one example row of real
  CMAB arm stats as an actual LaTeX table for legibility in print.

---

## Section: Deployment and Runtime Configuration

### Docker Compose Services, Networking, and Volumes
- What to write: services defined in the compose file (frontend/backend/db/adminer),
  networking between them, volumes for DB persistence, `watch` config for dev-mode live reload.
- Figure: **Infrastructure diagram** (checklist F) — primary placement here, matching
  `Architecture.md` §2's infrastructure ASCII diagram; Ch.5.1 can `\ref` this same figure
  instead of duplicating it.
- Table: good candidate — a small services/ports table (Frontend :5173, Backend :8001, DB
  :5433, Adminer :8080), pulled straight from the infra diagram's labels.

### Traefik Reverse Proxy, HTTPS, and Production Deployment
- What to write: Traefik routing rules (`api.{domain}` / `dashboard.{domain}`), automatic
  HTTPS/cert handling, what differs between the dev and production compose files.
- Figure: extend the same infrastructure diagram to show Traefik (already sketched in
  `Architecture.md` §2) rather than drawing a separate one.
- Table: not needed.

### Environment Configuration and Secrets
- What to write: `.env` usage, secret handling (DB password, JWT signing key), how these are
  injected via compose environment variables, and what's gitignored/dockerignored (ties to the
  `.dockerignore` you already have in the repo).
- Figure/table: not needed.

---

## Section: Implementation Challenges and Solutions

### CMAB State Persistence
- What to write: the challenge of storing a 23×23 matrix and a 23-vector per question as JSON,
  serialization/deserialization to/from numpy on each request, why JSON was chosen over a
  dedicated vector store or pickle (portability, readability, avoids O(n) history replay).
- Figure/table: not needed; a short before/after code snippet works well.

### Maintaining Question Selection Constraints
- What to write: enforcing the eligibility filter (role match + not-already-asked) correctly
  and efficiently on every request; edge case where the eligible pool runs out before the
  session budget is reached.
- **[PENDING-A]**: natural home for a forward-looking bullet on the adaptive-stopping design
  problem — "deciding when the system has found enough vs. needs to dig deeper" is itself an
  implementation challenge, even if the mechanism isn't built yet. Fine to preview this as
  "planned enhancement" framing rather than describing finished behavior.
- Figure/table: not needed.

### Synchronization Between Session State and Database
- What to write: keeping `questions_asked`, in-memory context building, and DB writes
  consistent; avoiding double-submission races; transaction boundaries around
  store-response + update-bandit-state + maybe-complete-session as one atomic unit.
- Figure/table: not needed.

### Frontend–Backend Integration Issues
- What to write: CORS configuration, whether types are generated from the OpenAPI schema to
  TypeScript (confirm from actual code), handling the polymorphic answer-submission response
  shape (`in_progress` vs. `completed`) on the frontend, error handling.
- Figure/table: not needed.

---

## Section: Chapter Summary
- What to write: recap what was actually built, tie back explicitly to the Chapter 4 design
  decisions (which parts of the design translated directly vs. needed adjustment during
  implementation), transition sentence into Chapter 6 (Evaluation Methodology).
- Figure/table: not needed.

---

## Open questions before we start writing prose

1. **Figure numbering**: Chapter 4 used `Arch_1.png`–`Arch_6_Sequence_diagram.png`. For
   Chapter 5's new figures (Infrastructure diagram, Technologies Used diagram, optionally the
   Context Vector diagram if placed here), do you want an `Impl_1.png`, `Impl_2.png`, … naming
   scheme, or continue the `Arch_` sequence?
2. **Context vector visual**: diagram or table (see CMAB Engine Implementation above) — your
   call, both are viable.
3. **Screenshots**: none of these exist yet per the checklist (Section E is entirely unchecked).
   Do you want to capture them now against the *current* implementation, or wait until the two
   pending changes land so the screenshots don't go stale immediately?
