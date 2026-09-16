# Master's Thesis Concept Presentation — "Recommendation System for ASPICE (SWE1-SWE6) Process Assessment"

> **Source:** `04_ConceptPresentation_2025_02_27.pdf` — the concept presentation given to
> class/supervisors at the start of the thesis. TU Chemnitz, Faculty of Computer Science,
> Professorship of Computer Engineering (Prof. Dr. Dr. h.c. Wolfram Hardt).
>
> **Student:** Faizan Ahmed, Automotive Software Engineering, faizan.ahmed@s2022.tu-chemnitz.de
> **Supervisors:** Prof. Dr. Dr. h.c. Wolfram Hardt (TUC, Computer Engineering); Dr.-Ing.
> Dimitrios Datsogiannis (TUC, Computer Engineering — co-author of both papers already
> captured in `supervisor_research_paper_new_approach_early_detection_vulnerabilities.md` and
> `supervisor_research_paper_recommender_systems_fault_rates.md`).
>
> **Note on the date field:** slide footers say "10/08/2026" while the source filename says
> `2025_02_27`. This is likely a template placeholder that was never updated on the slide
> master rather than the actual presentation date — don't treat "10/08/2026" as historically
> accurate without checking your own records.
>
> **Why this file matters more than a typical source note:** this is the **original plan**
> — what was promised/pitched before implementation began. Your own comment when providing
> it ("we will deviate what we promise in the start") flags that the actual build diverged
> from this pitch in some places. A **"Deviations & Evolution" section is included at the
> end** of this file, comparing every claim here against what `Architecture.md`, `README.md`,
> and `Implementation.md` show was actually built — this is exactly the material Ch.7.5
> (Reflection on Methodology) / Ch.8.3 (Limitations) needs, and it should also inform how you
> frame Ch.1 (don't let the introduction over-promise something the implementation chapters
> then contradict).

---

## Outline (as presented)

Introduction (Problem Statement, Motivation) → Objective → State of the Art →
Concept/Methodology → Implementation → Expected Results and Evaluation Criteria →
Conclusion → Milestones Plan → References

---

## 1. Introduction

Automotive Software Process Improvement and Capability dEtermination (ASPICE) is a process
assessment model used by car companies to evaluate how well a supplier develops software and
systems. It evaluates the quality of the development process. The Software Engineering
process group (SWE.1–SWE.6) covers the software V-model from requirements to verification.

**Figure 1 — "ASPICE SWE1–SWE6 aligned with the V-Model":** three horizontal pairs connected
by bidirectional arrows, forming the classic V shape: **[SWE.1] Requirements Analysis ↔
[SWE.6] Qualification Test** (outermost/top of the V), **[SWE.2] Architectural Design ↔
[SWE.5] Integration and Integration Test** (middle), **[SWE.3] Detailed Design and Unit
Construction ↔ [SWE.4] Unit Verification** (innermost/bottom of the V).

> Note: this figure labels SWE.6 as "Qualification Test," which is the SWE.6 name used in
> **ASPICE PAM v3.1**, not the current terminology. `aspice.md` (built from **PAM v4.0**)
> names it **"Software Verification."** Worth reconciling in Ch.2/Ch.4 — either note the
> version difference explicitly or simply use the v4.0 name consistently, since the rest of
> your project (Architecture.md, question bank) already follows v4.0 naming.

**Figure 2 — "Automotive SPICE process reference model [2]":** the full ASPICE v4.0 process
landscape diagram (identical in content to Figure 2 in `aspice.md` §3.1) — Supporting Process
Group (SUP.1/8/9/10/11), System Engineering Process Group (SYS.1–5), Validation Process Group
(VAL.1), Management Process Group (MAN.3/5/6), **Software Engineering Process Group (SWE) —
highlighted with a red box** showing SWE.1–SWE.6, Hardware Engineering Process Group (HWE.1–4),
Machine Learning Engineering Process Group (MLE.1–4), Process Improvement Process Group
(PIM.3), Acquisition Process Group (ACQ.4), Supply Process Group (SPL.2). The red highlight
box around SWE visually establishes the thesis's chosen scope within the full ASPICE
landscape — useful as a figure to reuse directly in Ch.1.5 (Scope of the Thesis) or Ch.2.1.2.

### Problem Statement
- ASPICE is mainly applied during **audits** rather than daily development.
- Process issues in requirements, design, coding, or testing are detected **too late**.
- **No continuous monitoring** after the audit to verify issue resolution.

### Motivation
- Reduce late discovery of process weaknesses.
- Make ASPICE useful during **daily development**, not only audits.
- Improve software quality and enable **earlier corrective actions**.

> This Problem Statement/Motivation pair is essentially the seed of your thesis's Ch.1.1/1.2
> — cross-check your current Introduction draft against this to make sure the "manual
> assessment pain point" framing you've been building (with the supervisor papers' citations)
> stays consistent with what was originally pitched here.

---

## 2. Objectives (as pitched)

1. Analysis and documentation of ASPICE SWE.1–SWE.6 for software process assessment.
2. Derivation, structuring of ASPICE criteria into a **weighted question database**.
3. Development of a **web-based framework** for continuous and automated ASPICE assessment.
4. Use of **Reinforcement Learning and Contextual Multi-Armed Bandits (CMAB)** for selecting
   the most relevant stakeholder questions.
5. Enablement of **early detection of software process weaknesses** and presentation of the
   results.

---

## 3. State of the Art (as pitched)

### ASPICE & Current Practice
- ASPICE is a standard for assessing automotive software processes (e.g., **PAM 4.0 – 2017**).
- ASPICE assessments are question-based and evaluate process capability using evidence and
  work products.
- In practice, assessments are mostly **periodic audits with manual evaluation**.
- Process weaknesses are often discovered late in development.

> **Factual correction to make in the thesis text:** the presentation says "PAM 4.0 – 2017."
> Per `aspice.md`'s own source document, **PAM v4.0 was released 2023-11-29** (a "Complete
> revision of PAM," per the PAM's own document history table); v3.1 was 2017. This looks like
> a slide typo conflating the version number with the wrong release year — fix this in the
> actual thesis text; don't propagate the 2017 date for v4.0.

### Related Research
- Software metrics and KPIs support quality measurement and early fault detection, but they
  are often **product-focused or late-stage focused**.
- A recent research approach (the 2024 supervisor paper) proposes a **dynamic survey model**:
  transform metrics into questions → assign weights and answer values → use reinforcement
  learning (CMAB) to ask only a few precise questions per cycle.

### Gap (as originally identified)
> "There is no automated, continuous, stakeholder-driven recommendation system specifically
> implementing ASPICE SWE.1–SWE.6 assessment."

> This is your **original, presentation-stage Research Gap statement** — compare it against
> whatever you've since written in Ch.3.6. It's narrower and cleaner than some later framing
> might have become; if your current Ch.3.6 draft has drifted from this crisp one-sentence
> gap, consider returning to it as the anchor.

### Comparison Table (as pitched — "State of the Art" slide 9)

| Aspect | ASPICE (Current Practice) | State of Art Research Paper (Dynamic Survey + CMAB) | This Thesis (Added value) |
|---|---|---|---|
| Assessment style | Manual, audit-driven | Continuous, question-driven | Continuous + ASPICE-aligned + web-based |
| Question-based evaluation | ✅ Yes (by auditors) | ✅ Yes (from metrics) | ✅ Yes (ASPICE base practices → questions) |
| Structured question database | ❌ Not standardized dataset | ✅ Generic questions for general software | ✅ New structured SWE.1–SWE.6 question bank |
| Focus on ASPICE SWE.1–SWE.6 | ✅ Defined in standard | ❌ Not SWE-specific (general automotive process focus) | ✅ Explicit SWE.1–SWE.6 mapping and evaluation |
| Automated question selection | ❌ No (human assessor selects) | ✅ Yes (CMAB selects few questions) | ✅ Yes (CMAB selects SWE questions per role) |
| Early feedback | ❌ Mostly late feedback | ✅ Yes (early evaluation) | ✅ Yes (early SWE weakness visibility) |

> **This table is directly reusable in Ch.3.5 (Cross-Comparison of Approaches)** — it's
> already exactly the three-way comparison structure that section needs (manual ASPICE vs.
> prior research vs. this thesis). Consider expanding it with a fourth column/row for the
> **2025 supervisor paper's algorithm-benchmarking contribution** (e-Greedy/LinUCB/Thompson
> Sampling comparison) if your Ch.3.5 wants to distinguish between the two supervisor papers
> rather than treating "State of Art Research Paper" as one undifferentiated prior work.

---

## 4. Concept / Methodology (as pitched)

- Online system evaluates ASPICE SWE.1–SWE.6 via targeted stakeholder questions.
- Questions cover **requirements, architecture, design/coding, and verification**.
- Uses dynamic survey with CMAB to select questions intelligently.

**Figure 3 — "Methodology" (pipeline diagram):** a linear sequence of 7 stages:
**ASPICE Domain Analysis (SWE.1–SWE.6)** → **Assessment Question Formulation** → **Scoring
Logic & Weighting Definition** → **Database Architecture & Integration** → **Intelligent
Question Selection (CMAB)** → **Web Application Development** → **Process Results
Visualization**.

> This pipeline is a clean, ready-made structure for **Ch.5 (Implementation)'s top-level
> narrative arc** — each of these 7 stages maps roughly onto a subsection: domain
> analysis→Ch.5.4.1 (base practice traceability), question formulation→Ch.5.4, scoring
> logic→Ch.5.2.4 (weakness classifier), database→Ch.5.2.2, CMAB→Ch.5.2.3, web app→Ch.5.3,
> visualization→Ch.5.3.3/7.4.1.

**Figure 4 — "Concept architecture [1]":** *(reproduced from the 2024 supervisor paper's Fig.
2, already described in full in
`supervisor_research_paper_new_approach_early_detection_vulnerabilities.md` §III.A)* —
Development Stakeholders + Manager + Software Versions → GUI → Model Controller ↔ Evaluation
Model, and Model Controller ↔ Recommendation System (RL Agent) ↔ Database (Q-Values, Question
Pool, Weights & Values, LUT, Evaluation Score, Context) → Results.

> **This confirms explicitly that the thesis's original architectural blueprint *was* the
> supervisor paper's own concept architecture diagram**, reused directly (citation [1] on the
> slide is the 2024 paper). Compare this against your **actual** implemented architecture in
> `Architecture.md` §2 (Layered Architecture Overview: Presentation → API → Business
> Logic/CMAB Engine/Classifier → Data) — see the Deviations section at the end of this file
> for how the two differ.

---

## 5. Implementation (as pitched)

### System Modules

**1. ASPICE SWE Question Bank (Database Module)**
- Extract auditor-relevant assessment criteria from SWE.1–SWE.6 base practices.
- Transform criteria into structured questions.
- Assign each question: stakeholder role(s) to answer; weights (importance) and predefined
  answer options (scoring).

**2. Web-Based Assessment Interface (GUI Module Integration)**
- Stakeholders log in and answer selected questions (short and fast survey).
- Supports repeated evaluation for each software release.

**3. Evaluation Controller (Scoring + Logic Module)**
- Converts answers into numeric values.
- Produces a **weakness classification per SWE process (e.g., good/medium/bad)** — i.e., a
  **3-category** classification scheme.
- Stores results and evidence.

**4. Recommendation Engine (ML Module: CMAB)**
- Selects the next best questions to ask based on: stakeholder context (role, project stage,
  release scope); previous responses (partial feedback); question weights.

**5. Results Dashboard (Reporting Module)**
- Displays current process weaknesses by SWE.1–SWE.6 and trends across releases.
- Supports early detection of weak areas **before defects become visible via tickets**.

### Algorithms (as pitched)

**Algorithm A — Release Assessment Workflow:**
1. Start new release session
2. Get stakeholder context (role, release scope)
3. CMAB selects **top-k questions** *(plural — multiple questions selected per pass)*
4. Stakeholder answers questions
5. Convert answers to scores
6. Aggregate per SWE.1–SWE.6
7. Classify Good/Medium/Bad and store results.

**Algorithm B — CMAB Question Selection:**
1. For each question *q*, estimate expected reward based on context
2. Select question set *Q* (explore/exploit balance)
3. Receive answer value as reward
4. Update model parameters for future selections.

**Figure 5 — "Recommendation System for ASPICE"** *(a two-box diagram)*: left box "Software
Engineering Process Group (SWE)" showing the V-model pairing **SWE.1 (Requirements) →
SWE.6 (Software Test)**, **SWE.2 (Architecture) → SWE.5 (Integration Test)**, **SWE.3
(Design/Code) → SWE.4 (Unit Test)** with arrows flowing into a right box "Recommendation
System" containing three labeled components: **Data Bank of Relevant Questions** ("Curates
most relevant questions to assess process maturity"), **Web-based Interface** ("Provides
continuous feedback and quality classification"), **Evaluation Model** ("Selects the right
questions for the right stakeholders").

> **Important design-evolution point:** the pitched Algorithm A/B describes selecting a
> **question *set*** (top-*k*, plural) per round — matching the supervisor papers' own
> "5 questions per round" pattern. Your **actual implemented** `audit_service.py`/
> `cmab_engine.py` selects **one question at a time**, sequentially, rebuilding the context
> vector after every single answer (per `Implementation.md` §4: "Next question selected —
> the context vector is rebuilt... and the next question is chosen" — one question per
> step, not a batch). This is a legitimate and probably *better* design (fresher context per
> selection) but it is a **deviation from what was pitched** — see the Deviations section.

### Technologies (as pitched)

- **Frontend:** ReactJS (UI for stakeholders)
- **Backend:** Python (business logic, evaluation controller)
- **Database:** MySQL **or** Postgres (question bank, users/roles, results)
- **Machine Learning:** Reinforcement Learning (Contextual Multi-Armed Bandits – CMAB)
- **API & Integration:** REST API (communication between frontend and backend)
- **Deployment (optional):** Docker
- **Version Control:** Git (change tracking)

**Figure 6 — "Technologies Used":** a block diagram — ReactJS at top, connected to MySQL
(left) and a REST API (center) which connects to RL Agent - CMAB and Recommendation System
(right); Python sits below the REST API and connects to both the API and (separately) to Git
and Docker at the bottom.

> Compare against your **actual** stack (`README.md`): FastAPI (not just "Python"), SQLModel
> ORM, **PostgreSQL specifically** (not "MySQL or Postgres"), React 18 + TypeScript + Vite +
> TanStack Router + Tailwind + shadcn/ui (far more specified than "ReactJS"), JWT auth (not
> mentioned at all in the pitch), Docker Compose as the **core** dev workflow (not "optional").
> See Deviations section.

---

## 6. Expected Results (as pitched)

- A structured and weighted ASPICE SWE.1–SWE.6 question bank (auditor-style questions mapped
  to SWE processes and stakeholder roles).
- A web-based recommendation system that selects a small number of well-targeted questions per
  evaluation cycle.
- Automatic process weakness classification (**Good / Medium / Bad**) for each SWE process
  (SWE.1–SWE.6).
- A dashboard that provides early visibility of process weaknesses and trends across software
  releases.

## 7. Evaluation / Testing Scheme (as pitched)

- **Content validation** (with supervisor): check question relevance, clarity, SWE coverage,
  and correct mapping to stakeholder roles.
- **Functional testing:** end-to-end testing of the web system (question selection → answering
  → scoring → dashboard).
- **Scoring validation:** verify correct classifications with controlled test cases.
- **Recommendation evaluation:** assess efficiency and improvement of question selection over
  time.
- *(Exact thresholds, weights, baselines, and success metrics explicitly left "to be finalized
  and discussed with the supervisor" at pitch time.)*

> This four-part testing scheme maps directly onto your current Ch.6 structure: content
> validation → (not yet documented as a formal step — check whether this happened and how);
> functional testing → Ch.6.3 (Functional and Smoke Testing); scoring validation → Ch.6.2/6.5
> (Unit Testing, Weakness Score Distributions); recommendation evaluation → Ch.6.5/7.3 (CMAB
> Arm Statistics). Good cross-check that your Ch.6 methodology fulfills everything pitched
> here — and if "content validation with supervisor" didn't happen as a discrete documented
> step, that's worth naming as a limitation (it directly echoes the "expert-validated
> weights" gap already flagged in the 2025 supervisor paper's `.md` file).

## 8. Conclusion (as pitched)

- Bridges the gap between periodic ASPICE audits and continuous process monitoring in
  automotive software development.
- Implements an online question-based system for assessing SWE.1–SWE.6, covering
  requirements, design, coding, and verification.
- Uses a structured question bank with CMAB-based Reinforcement Learning to detect process
  weaknesses early.
- Improves transparency, provides early feedback, reduces late-stage defects, and supports
  automated process assessment.

## 9. Milestones Plan (as pitched — Gantt chart, Figure 7)

| Task | Duration | Approx. window |
|---|---|---|
| ASPICE Literature & Standards Review | 4 weeks | March |
| Concept & Design of Recommendation System | 2 weeks | April |
| **Concept Presentation & Feedback** *(milestone)* | — | 13 March |
| Database Schema Creation & Hosting | 1 week | April |
| Transform ASPICE Parameters to Questions | 2 weeks | April |
| Populate ASPICE Question Database | 1 week | April/May |
| Backend Architecture & API Development | 3 weeks | May |
| ML Question Selection Integration | 1 week | May/June |
| Frontend–Backend System Integration | 2 weeks | June |
| System Testing & Supervisor Verification | 2 weeks | June/July |
| **Table of Content, List of References** *(milestone)* | — | 12 June |
| Report Writing | 4 weeks | July/August |
| **Submission of Pre-version** *(milestone)* | — | 10 July |
| Correction | 1 week | August |
| Time Buffer | 1 week | August |
| **Final Submission** *(milestone)* | — | 31 July *(sic — appears in the row after "Time Buffer," likely a transcription/ordering quirk in the original slide; verify actual planned final-submission date against your own records)* |

> **This is the single most useful artifact in this file for your Ch.7.2 (Reflection on
> Methodology)** — a documented original schedule to compare against what actually happened.
> Given the current session context (thesis ~70% implemented as of your own note, and you're
> now in the writing phase in what appears to be August 2026), it's worth explicitly writing
> a short paragraph in Ch.7.2 comparing planned vs. actual timeline — schedule slippage is a
> completely normal and expected thing to reflect on in a methodology chapter, not something
> to hide.

## 10. References (as cited in the presentation)

`[1]` D. Datsogiannis, A. Heller, and W. Hardt, "A New Approach for Early Detection of
Vulnerabilities Across the Automotive Software Development," in *Proc. Int. Symp. Comput.
Sci. Educ. Technol. (ISCSET)*, 2024, DOI: 10.1109/ISCSET58624.2024.10807908. *(= reference
[1]/`datsogiannis2024early` in `references.md`.)*

`[2]` VDA QMC, *Automotive SPICE® Process Assessment Model (PAM), Version 4.0*. Germany:
Verband der Automobilindustrie (VDA) Quality Management Center (QMC), 2023. *(=
`vdaqmc2023pam` in `references.md`.)*

`[3]` L. Li, W. Chu, J. Langford, and R. E. Schapire, "A contextual-bandit approach to
personalized news article recommendation," in *Proc. 19th Int. Conf. World Wide Web (WWW)*,
2010, pp. 661–670. *(= `li2010contextual` in `references.md` — the seminal LinUCB paper.)*

`[4]` Z. H. Martinez, P. M. Moreno, J. A. Vergara Camacho, and G. C. Vega, "Study on the use
of defect metrics in the software development process. flaws and vulnerabilities," in *2023
IEEE International Conference on Engineering Veracruz (ICEV)*, 2023, pp. 1–7. *(=
`martinez2023defectmetrics`.)*

`[5]` S. Zhong, W. Ying, X. Chen, and Q. Fu, "An Adaptive Similarity-Measuring-Based CMAB
Model for Recommendation System," *IEEE Access*, vol. 8, pp. 42550–42561, 2020. *(=
`zhong2020adaptivecmab`.)*

`[6]` T. B. Alakus, R. Das, and I. Turkoglu, "An overview of quality metrics used in
estimating software faults," in *2019 International Artificial Intelligence and Data
Processing Symposium (IDAP)*, 2019, pp. 1–6. *(= `alakus2019qualitymetrics`.)*

`[7]` C. Murphy, "Automotive SPICE: 0-60 in No Time Flat," *IEEE Engineering Management
Review*, vol. 47, no. 2, pp. 26–28. *(= `murphy_aspice_0to60`.)*

`[8]` A. Haghighatkhah, M. Oivo, A. Banijamali, and P. Kuvaja, "Improving the state of
automotive software engineering," *IEEE Software*, vol. 34, no. 5, pp. 82–86, 2017. *(=
`haghighatkhah2017improving`.)*

`[9]` Y. Jiang, J. Lin, B. Cukic, S. Lin, and Z. Hu, "Replacing code metrics in software fault
prediction with early life cycle metrics," in *2013 IEEE Third International Conference on
Information Science and Technology (ICIST)*, IEEE, 2013, pp. 516–523. *(=
`jiang2013earlylifecycle`.)*

`[10]` M. Naeem, S. T. H. Rizvi, and A. Coronato, "A gentle introduction to reinforcement
learning and its application in different fields," *IEEE Access*, vol. 8, pp. 209320–209344,
2020. *(= `naeem2020gentleintro`.)*

`[11]` S. Shahrampour, A. Rakhlin, and A. Jadbabaie, "Multi-armed bandits in multi-agent
networks," in *2017 IEEE International Conference on Acoustics, Speech and Signal Processing
(ICASSP)*, 2017, pp. 2786–2790. *(= this reference was **not yet included** in
`references.md` — it appears in the 2024 supervisor paper's list too (ref. [25] there) but
was dropped from your curated 50 as one of the "narrower SFP-adjacent" exclusions. Since it's
directly cited in your own concept presentation, consider re-adding it to `references.md`
Section F.)*

`[12]` N. Gutowski, T. Amghar, O. Camp, and F. Chhel, "Context enhancement for linear
contextual multi-armed bandits," in *2018 IEEE 30th International Conference on Tools with
Artificial Intelligence (ICTAI)*, 2018, pp. 1048–1055. *(= `gutowski2018contextenhancement`.)*

`[13]` "Automotive-spice." [Online]. Available: https://vda-qmc.de/en/automotive-spice/ *(=
`vdaqmc_website`.)*

> **Reference-list note:** 12 of these 13 references are already in `references.md`; only
> **[11] Shahrampour et al.** is missing from the curated 50 — since it's cited directly in
> your own concept presentation (not just in a supervisor paper), it's worth adding back so
> your reference list stays internally consistent with what you've already told your
> supervisor you'd cite.

---
