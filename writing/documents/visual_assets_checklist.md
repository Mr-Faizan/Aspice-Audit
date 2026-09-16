# Visual Assets Checklist — Figures, Tables, Graphs, Screenshots

> A complete inventory of every visual asset worth having in the thesis, organized by where
> it comes from and what you need to do to get it. Check items off as you collect them.
>
> **Copyright/citation note:** figures reproduced from the PAM and both supervisor papers are
> copyrighted (VDA / IEEE respectively). Reproducing them in a thesis for academic purposes
> with a clear source citation under the figure (e.g., "Source: adapted from [18], Fig. 2")
> is standard, expected academic practice — just never present them as your own uncredited
> work. For the PAM figures specifically, prefer **redrawing** them cleanly (they're simple
> box/table diagrams) over screenshotting the PDF, since a redrawn version looks sharper in
> print and you can trim it to exactly the SWE-relevant subset.

---

## A. Figures & Tables to extract from the ASPICE PAM v4.0 PDF

Source: `Automotive-SPICE-PAM-v40.pdf`. Page numbers refer to the PDF as read into `aspice.md`.

- [ ] **Fig. 1 (p.14)** — Process assessment model relationship (Measurement framework ↔
  PAM ↔ PRM triangle). → Ch.2.1.1, explaining the two-dimensional capability framework.
- [ ] **Fig. 2 (p.15)** — Automotive SPICE process reference model, full overview (all
  process groups). → Ch.1.5 (Scope) / Ch.2.1.2 — **essential**, this is the standard figure
  every ASPICE thesis needs once, to show where SWE sits in the whole landscape.
- [ ] **Fig. 3 (p.25)** — Relationship between assessment indicators and process capability
  (the CL1–CL5 ladder with GP/BP/II arrows). → Ch.2.1.3, explaining base vs. generic
  practices.
- [ ] **Fig. 4 (p.27)** — Levels of abstraction for the term "process" (What / How / Doing).
  → Ch.2.1/Ch.4.9, good visual support for "why the PAM doesn't prescribe a fixed workflow."
- [ ] **Fig. 5 (p.28)** — Performing a process assessment for determining process capability
  (3-step: Execution → Methods → PAM). → Ch.2.1/Ch.6 methodology framing.
- [ ] **Table 14 (p.18–19)** — Process capability levels (0–5 with descriptions). →
  Ch.2.1.3/Ch.4.6 — **essential**, cite/reproduce as a real table, not prose.
- [ ] **Table 15 (p.19)** — Process attributes (PA 1.1–5.2) mapped to capability levels. →
  Ch.2.1.3.
- [ ] **Table 16 (p.20)** — Rating scale (N/P/L/F definitions). → Ch.2.1.3, and directly
  useful as a comparison point against your own 0–4 weight scale / 4-band weakness
  thresholds (Ch.4.9).
- [ ] **Table 20 (p.23)** — Capability level model (which PA ratings are required at each
  level). → Ch.2.1.3, optional but thorough.
- [ ] **Annex Fig. C.2 (p.144)** — "Element, Component, and Unit" (SYS/SWE V-model nesting
  diagram, already described in full in `aspice.md` §9.1). → Ch.2.1.2/Ch.4.4, explains why
  SWE.3/4 operate at unit level vs. SWE.2/5 at component level — **redraw this one**, it's
  genuinely useful and simple to reproduce cleanly.
- [ ] **Annex Fig. C.5/C.6 (p.150)** — "Agree" vs. "Summarize and Communicate" diagram
  (already described in `aspice.md` §9.2). → Ch.4.4.1, supports your question-bank
  `recommendation_logic` phrasing rationale if you use it.
- [ ] *(Optional)* **Annex Fig. C.1 (p.143)** — The "Plug-in" concept (SYS core + domain
  plug-ins). → Ch.1.5, an alternative/additional scope-framing figure to Fig. 2 above.

---

## B. Figures & Table from the 2024 supervisor paper

Source: `supervisor_research_paper_new_approach_early_detection_vulnerabilities.md` (full
descriptions already captured there — go back to the actual PDF to extract/screenshot the
real image at full resolution).

- [ ] **Fig. 1** — Product life cycle of a vehicle (Development/Software Updates/
  Production/Operation & Maintenance timeline). → Ch.1.1 Motivation — nice opening visual.
- [ ] **Fig. 2** — Concept architecture (Stakeholders/Manager/GUI/Model Controller/RL
  Agent/Database). → Ch.3 Related Work, and as an explicit **before/after comparison**
  against your own actual architecture diagram in Ch.4.2.
- [ ] **Fig. 3 (a table, captioned as a figure)** — "Automotive SPICE process groups [18]" —
  SYS/SWE/VAL/PIM processes they analyzed. → Ch.3.4 Cross-Comparison, shows their broader
  4-group scope vs. your SWE-only focus.
- [ ] **Fig. 4** — Structure of an evaluation packet (Question ID → Roles → Weight →
  Payload → Answers → Values → Targets → Given Answer). → Ch.3/Ch.4.4, compare against your
  own `AuditQuestion`/`AuditOption` schema.
- [ ] **Fig. 5** — CMAB workflow (Explore → Join Service → Learn Online → Deploy, cyclic). →
  Ch.2.3.2, the standard online-bandit-serving-loop diagram — good generic explainer figure.

---

## C. Figures & Table from the 2025 supervisor paper

Source: `supervisor_research_paper_recommender_systems_fault_rates.md`.

- [ ] **Fig. 1** — Process of bug finding and fixing in relation to time (swimlane with
  bugfixing feedback loop). → Ch.1.1/1.2 Motivation — **strong, high-impact figure**, the
  defect-cost-over-time argument in one picture.
- [ ] **Fig. 2** — Literature review and findings extraction funnel (4 category columns →
  database). → Ch.3, shows their question-sourcing methodology vs. your ASPICE-only sourcing.
- [ ] **Fig. 3** — 0% vs. 30% changing-rate scenario comparison (Project X vs. Project Y). →
  Ch.8.4.2 (Future Work) if you discuss simulation-based benchmarking as a next step.
- [ ] **Fig. 4** — Tuning-parameter selection tree (4 use cases × 3 algorithms). → Ch.7.5/7.6
  Discussion, directly relevant to your own fixed α = 1.0 choice.
- [ ] **Fig. 5** — Cumulative rewards line chart (4 epsilon values). → Ch.7 Discussion.
- [ ] **Fig. 6** — Average rewards line chart (convergence over 1000 rounds). → Ch.7
  Discussion, good example of "rounds needed to reach stable performance" framing.
- [ ] **Fig. 7** — Reward distribution pie chart (4 bands: above 0.75 / 0.5–0.75 / 0.25–0.5 /
  up to 0.25). → Ch.7 Discussion — note this is a **3-way split scheme conceptually similar**
  to your own weakness-score bands; a nice one-to-one visual comparison opportunity.
- [ ] **Table I** — Full evaluation results (algorithm × use case × tuning parameter × reward
  bands). → Ch.7.6 Discussion — **the single most important table to reproduce**, since it's
  the concrete evidence for the "e-Greedy beat LinUCB" finding you need to address.

---

## D. Figures from your own concept presentation

Source: `concept_presentation.md`. These are yours already — just re-export them from the
original PPTX/PDF at full resolution rather than screenshotting the class PDF.

- [ ] **Figure 1** — SWE.1–SWE.6 aligned with the V-Model. → Ch.1.5/Ch.2 — **redraw with the
  PAM v4.0 name for SWE.6** ("Software Verification," not "Qualification Test" — see the
  naming-drift note in `concept_presentation.md` §1).
- [ ] **Figure 2** — Process reference model with the SWE group highlighted in a red box. →
  Ch.1.5 Scope — genuinely excellent scope-framing figure, better than the plain PAM Fig. 2
  for this purpose since the highlight does the "here's what we cover" work visually.
- [ ] **Figure 3** — Methodology pipeline (7 stages: Domain Analysis → ... → Results
  Visualization). → Ch.4/Ch.5, a clean top-level structure diagram for your implementation
  chapter's narrative.
- [ ] **Figure 5** — "Recommendation System for ASPICE" box diagram (SWE V-model → Data
  Bank/Web Interface/Evaluation Model). → Ch.4.2, an alternative simplified architecture
  view alongside your detailed layered-architecture diagram.
- [ ] **Figure 6** — Technologies Used diagram (ReactJS/MySQL/Python/REST API/RL Agent/
  Git/Docker). → Ch.5.1 — **redraw with your actual stack** (FastAPI, PostgreSQL/SQLModel,
  React+TS+Vite+TanStack, JWT, Docker Compose) rather than reusing the pitched generic one.
- [ ] **Figure 7** — Gantt chart milestones plan. → Ch.7.2 Reflection on Methodology — use
  as the "planned" half of a planned-vs-actual timeline comparison.

---

## E. Screenshots to capture yourself from the running application

Nothing to download — start the app (`docker compose watch`) and capture these directly.
Use a consistent browser window size and consider light mode for print legibility.

- [ ] Signup page, showing the stakeholder-role dropdown (7 roles visible).
- [ ] Login page.
- [ ] Audits/dashboard list page (start/continue/view-results options).
- [ ] Audit session screen mid-flow — a question with options A–E and the "Question X of 12"
  progress bar visible.
- [ ] Results page — radar chart (SWE.1–6).
- [ ] Results page — heatmap table (process × level, color-coded green/yellow/orange/red).
- [ ] Results page — top-3-weaknesses list with recommendation text.
- [ ] History page — table of past sessions.
- [ ] Admin — Question Bank Manager (list view with process/level/role filters).
- [ ] Admin — a single question's edit/detail view (showing options A–E and weights).
- [ ] Admin — Analytics Dashboard: aggregate weakness heatmap across all sessions.
- [ ] Admin — Analytics Dashboard: CMAB arm performance table (pull count, avg reward).
- [ ] Admin — Analytics Dashboard: user participation stats (sessions by role).
- [ ] *(Optional)* Swagger/OpenAPI docs page (`/docs`) — nice for Ch.5 API implementation.
- [ ] *(Optional)* A terminal screenshot of `docker compose watch` running all services, for
  Ch.5.1 (Development Environment).

---

## F. Diagrams you need to (re)draw yourself — not sourced anywhere, must create

These describe your own system and don't exist as ready-made images yet — only as ASCII art
in `Architecture.md` or prose in `Implementation.md`. Redraw them properly (e.g., in
draw.io/Excalidraw/PowerPoint, or as a Mermaid diagram if your thesis tooling supports it).

- [ ] **System architecture diagram** — layered view (Presentation → API → Business
  Logic/CMAB Engine/Classifier → Data), from `Architecture.md` §2. → Ch.4.2 — your single
  most important original figure.
- [ ] **Infrastructure diagram** — Docker Compose topology (Frontend/Backend/DB/Adminer/
  Traefik), from `Architecture.md` §2. → Ch.4.2/Ch.5.5.
- [ ] **Entity-Relationship diagram** — User, AuditQuestion, AuditOption, AuditSession,
  AuditResponse, WeaknessResult, BanditArmState and their relationships, from
  `Architecture.md` §3. → Ch.4.4 — essential, currently only exists as a text arrow diagram.
- [ ] **Sequence diagram** — the answer-submission flow (validate → store response → compute
  reward → update bandit → select next question or complete session), from
  `Architecture.md` §6. → Ch.4.7.4 — this is explicitly named as a figure in your own ToC
  already (4.7.4 "Core Answer-Submission Sequence Diagram").
- [ ] **Context vector diagram** — a labeled bar/table showing the 23 dimensions (7 role +
  1 progress + 6 process-coverage + 3 level-coverage + 6 running-score), from
  `Implementation.md` §2.3. → Ch.4.5.2 — makes an abstract vector concrete and visual.
- [ ] **LinUCB formula callout** — typeset the UCB score equation
  (`UCB = θᵀx + α·√(xᵀA⁻¹x)`) as a clean boxed/numbered equation. → Ch.2.3.3/Ch.4.5.4 (this
  is standard LaTeX math, not an "image," but plan the numbering/placement now).
- [ ] **Update-rule callout** — `A ← A + xxᵀ`, `b ← b + reward·x`, similarly typeset. →
  Ch.4.5.6.
- [ ] **Session flow diagram** — the "Session flow (How an Audit Works)" 7-step list from
  `Implementation.md` §4, turned into an actual flowchart rather than a numbered list. →
  Ch.4.8.2.

---

## G. Result charts to generate once you have real pilot-session data

These can't exist yet — they depend on the pilot sessions your Ch.6 methodology plans to run.
Plan the code/notebook that will produce each one now so you're not scrambling later.

- [ ] Radar chart(s) — one or two representative real sessions (already produced live by the
  app itself; just screenshot a real result rather than a mock one).
- [ ] Aggregate weakness heatmap across all pilot sessions (from `/analytics/weaknesses`).
- [ ] CMAB bandit-arm statistics — bar chart of pull count and average reward per question
  (from `/analytics/bandit`). → Ch.7.3.2 — your evidence for real (non-simulated) CMAB
  behavior, directly answering what the 2025 supervisor paper left to simulation only.
- [ ] Process-coverage chart — how many of the 6 SWE processes got covered within the
  12-question budget, across sessions. → Ch.7.3.3.
- [ ] Weakness score distribution histogram (all 18 process×level cells, across sessions). →
  Ch.7.4.
- [ ] API response latency chart (if you run a basic performance check). → Ch.7.5.1.
- [ ] Session completion time — a simple bar/box comparison if you have any manual-assessment
  timing data to compare against. → Ch.7.5.2 (optional, only if data exists).

---

## Summary count

- **A (PAM):** 12 items — extract/redraw from the standard PDF.
- **B (2024 paper):** 5 items — extract from that PDF.
- **C (2025 paper):** 8 items — extract from that PDF, incl. the critical Table I.
- **D (your pitch):** 6 items — re-export from your own slides, two need correction/redraw.
- **E (app screenshots):** 13–15 items — capture from the running app now.
- **F (original diagrams):** 8 items — must be created, none exist yet.
- **G (result charts):** 7 items — depend on pilot data, plan the generation code now.

**Total: ~55 visual assets** if you collect everything here — comfortably more than enough
for a visually rich thesis. If you need to prioritize, do **E and F first** (they're fully in
your control and don't depend on anything external), then **A/B/C** (quick PDF exports), and
treat **G** as an ongoing task alongside your pilot sessions in Ch.6.
