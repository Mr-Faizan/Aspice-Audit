# ASPICE SWE.1–SWE.6 Question Bank

A structured, weighted question bank derived from the Automotive SPICE SWE.1–SWE.6 base practices. **60 questions**, **300 answer options**, each option carrying a weight from `0` (best / lowest risk) to `5` (worst / highest risk).

## Legend

**Weight**

| Weight | Meaning |
|:---:|---|
| `0` | Best / lowest risk |
| `5` | Worst / highest risk (highest CMAB reward) |

**Stakeholder codes**

| Code | Stakeholder |
|:---:|---|
| `SD` | Software Developer |
| `SA` | Software Architect |
| `PM` | Project Manager |
| `QA` | QA Engineer |
| `TE` | Test Engineer |
| `TL` | Team Lead |
| `ASR` | ASPICE Assessor |

**Capability levels**

| Level | Meaning |
|:---:|---|
| `L1` | Performed |
| `L2` | Managed |
| `L3` | Established |

## Contents

- [SWE.1 — Software Requirements Analysis](#swe1-software-requirements-analysis) (12 questions)
- [SWE.2 — Software Architectural Design](#swe2-software-architectural-design) (11 questions)
- [SWE.3 — Software Detailed Design and Unit Construction](#swe3-software-detailed-design-and-unit-construction) (9 questions)
- [SWE.4 — Software Unit Verification](#swe4-software-unit-verification) (9 questions)
- [SWE.5 — Software Component Verification and Integration Verification](#swe5-software-component-verification-and-integration-verification) (10 questions)
- [SWE.6 — Software Verification](#swe6-software-verification) (9 questions)

---

## SWE.1 — Software Requirements Analysis

### `SWE1_L1_01` · Level L1 (Performed) · `SWE.1.BP1`

**Base practice:** SWE.1.BP1 — Specify SW requirements (verifiability, unambiguity)

**Question:** How are software requirements specified for the current release?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Each requirement is uniquely identified, atomic, verifiable and references its source | 0 |
| B | Requirements are uniquely identified but verifiability criteria are missing for some | 2 |
| C | Requirements exist as free-text paragraphs without unique IDs | 3 |
| D | Requirements are partially captured in slides/e-mails | 4 |
| E | No formal SW requirements set exists | 5 |

- **Identifies:** Weak requirement quality, ambiguity, untestable SW requirements
- **Stakeholders:** SA, SD, QA
- **Recommendation logic:** High weight ⇒ recommend a requirement-specification template aligned with IEEE 29148 + tooling audit (DOORS/Polarion/Jama).

### `SWE1_L1_02` · Level L1 (Performed) · `SWE.1.BP2`

**Base practice:** SWE.1.BP2 — Structure SW requirements

**Question:** How are SW requirements categorised and prioritised?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Categorised (functional/non-functional/safety/security) and prioritised against release plan | 0 |
| B | Categorised only | 2 |
| C | Prioritised only | 2 |
| D | Done ad-hoc per request | 4 |
| E | Not categorised or prioritised | 5 |

- **Identifies:** Missing prioritisation / categorisation, scope-creep risk
- **Stakeholders:** PM, SA
- **Recommendation logic:** Recommend introducing a categorisation scheme + MoSCoW/RICE prioritisation linked to MAN.3 (out of scope but referenced).

### `SWE1_L1_03` · Level L1 (Performed) · `SWE.1.BP3`

**Base practice:** SWE.1.BP3 — Analyse SW requirements (correctness, technical feasibility)

**Question:** How is the technical feasibility of new SW requirements analysed before they are baselined?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Formal feasibility review with architect & developer sign-off | 0 |
| B | Informal feasibility check by architect only | 2 |
| C | Feasibility judged during implementation | 4 |
| D | Feasibility never explicitly checked | 5 |
| E | Unknown / no defined approach | 5 |

- **Identifies:** Latent feasibility risk, late re-work
- **Stakeholders:** SA, SD
- **Recommendation logic:** Recommend a feasibility-review checklist gated on requirement baselining.

### `SWE1_L1_04` · Level L1 (Performed) · `SWE.1.BP4`

**Base practice:** SWE.1.BP4 — Analyse impact on operating environment

**Question:** When SW requirements affect timing, memory, or operating-environment behaviour, how is the impact captured?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Documented impact analysis linked to each affected requirement | 0 |
| B | Captured in design notes only | 2 |
| C | Discussed verbally in reviews | 3 |
| D | Not analysed unless a defect is found | 4 |
| E | No process | 5 |

- **Identifies:** Missed timing / ODD / resource impact
- **Stakeholders:** SA, SD
- **Recommendation logic:** Recommend introducing impact-analysis fields in the requirement template; cross-link to non-functional verification in SWE.6.

### `SWE1_L1_05` · Level L1 (Performed) · `SWE.1.BP5`

**Base practice:** SWE.1.BP5 — Ensure consistency & bidirectional traceability (SYS-req ↔ SW-req ↔ SYS-arch)

**Question:** What is the current state of bidirectional traceability between system requirements and software requirements?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Tool-enforced bidirectional links, audited every release | 0 |
| B | Bidirectional links exist but coverage is partial | 2 |
| C | Only forward links (SYS→SW) exist | 3 |
| D | Traceability is maintained in spreadsheets | 4 |
| E | No traceability data | 5 |

- **Identifies:** Broken bidirectional traceability — top assessor finding
- **Stakeholders:** SA, QA, ASR
- **Recommendation logic:** High signal: recommend RTM/OSLC tooling audit and a SUP.10 change-impact review procedure (referenced, not in scope).

### `SWE1_L1_06` · Level L1 (Performed) · `SWE.1.BP6`

**Base practice:** SWE.1.BP6 — Communicate agreed SW requirements & impact

**Question:** How is agreement on the SW requirements baseline reached and recorded?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Formal review meeting with signed-off minutes per release | 0 |
| B | Review meeting without recorded sign-off | 2 |
| C | E-mail confirmation only | 3 |
| D | Implicit agreement, no record | 4 |
| E | No agreement step | 5 |

- **Identifies:** Lack of agreement → late churn
- **Stakeholders:** PM, SA, TL
- **Recommendation logic:** Recommend introducing a lightweight "Requirements Agreement Record" gate.

### `SWE1_L1_08` · Level L1 (Performed) · `SWE.1.BP5`

**Base practice:** SWE.1.BP5 — Ensure consistency & bidirectional traceability (SW-req ↔ system architecture)

**Question:** How is bidirectional traceability maintained between software requirements and the system architecture (i.e., allocation of SW requirements to system architecture elements)?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Tool-enforced allocation links, reviewed and audited each baseline | 0 |
| B | Allocation links exist but are not audited | 2 |
| C | Allocation documented in a spreadsheet, maintained manually | 3 |
| D | Allocation implicit / known only to individual engineers | 4 |
| E | No traceability to system architecture exists | 5 |

- **Identifies:** Missing allocation of SW requirements to system architecture elements
- **Stakeholders:** SA, QA, ASR
- **Recommendation logic:** Distinct from SYS-req↔SW-req traceability (SWE1_L1_05) — BP5 covers two separate outcomes (O5, O6) and only O5 was previously asked. A gap here means SW requirements may not be correctly scoped to their allocated system-architecture element. Recommend extending the RTM with a system-architecture allocation column.

### `SWE1_L1_09` · Level L1 (Performed) · `SWE.1.BP3`

**Base practice:** SWE.1.BP3 — Analyse SW requirements (interdependencies)

**Question:** How are dependencies and potential conflicts between software requirements identified and managed?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Dependencies explicitly modelled/tagged and conflict-checked at each baseline review | 0 |
| B | Dependencies documented but not systematically conflict-checked | 2 |
| C | Dependencies identified informally during design | 3 |
| D | Dependencies surface only when a defect/integration issue occurs | 4 |
| E | Not analysed | 5 |

- **Identifies:** Conflicting or circular requirement dependencies undetected until late
- **Stakeholders:** SA, SD, QA
- **Recommendation logic:** BP3 covers correctness, feasibility, and interdependencies; SWE1_L1_03 already covers feasibility, this closes the interdependency sub-aspect. Recommend a dependency/conflict tag in the requirements tool plus a conflict-check step in the review checklist.

### `SWE1_L2_07` · Level L2 (Managed) · `GP 2.1.1, GP 2.1.2`

**Base practice:** GP 2.1.1, GP 2.1.2 — Performance objectives & planning for SWE.1

**Question:** How is the SWE.1 process planned and monitored at project level?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Documented requirements-engineering plan with KPIs (e.g., review backlog, churn) reviewed monthly | 0 |
| B | Plan exists but KPIs are not tracked | 2 |
| C | Activities scheduled in MS-Project only | 3 |
| D | Planned ad-hoc per sprint | 4 |
| E | No plan | 5 |

- **Identifies:** Missing/weak strategy for the requirements process
- **Stakeholders:** PM, QA
- **Recommendation logic:** Indicates PA 2.1 weakness; recommend a requirements KPI dashboard.

### `SWE1_L2_10` · Level L2 (Managed) · `GP 2.1.6`

**Base practice:** GP 2.1.6 — Manage interfaces between involved parties (SWE.1)

**Question:** How are interfaces between software requirements engineers and other involved parties (system engineering, safety, customer) coordinated for requirement changes?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Defined communication mechanism with assigned responsibilities and change-notification SLA | 0 |
| B | Communication mechanism exists but responsibilities not assigned | 2 |
| C | Coordination happens through periodic status meetings only | 3 |
| D | Coordination happens only when a conflict is discovered | 4 |
| E | No defined coordination mechanism | 5 |

- **Identifies:** Poor coordination between requirements engineering and system engineering / other stakeholders
- **Stakeholders:** SA, PM, TL
- **Recommendation logic:** Complements SWE1_L1_06 (one-time agreement) and SWE1_L2_07 (planning/KPIs); recommend a stakeholder communication matrix analogous to SWE5_L2_07's interface change board.

### `SWE1_L2_11` · Level L2 (Managed) · `GP 2.2.1–2.2.3`

**Base practice:** GP 2.2.1–2.2.3 — Work-product requirements, storage and control (SW requirements)

**Question:** How are the software requirement work products stored, versioned, and status-controlled (e.g., Under Work / Reviewed / Released)?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Versioned in requirements-management tool with a defined status workflow and baseline history | 0 |
| B | Versioned in tool but no formal status workflow | 2 |
| C | Stored in a shared drive/document, manually versioned | 3 |
| D | Stored locally by individual engineers | 4 |
| E | Not under any storage/version control | 5 |

- **Identifies:** Requirements work products not under configuration/status control
- **Stakeholders:** QA, ASR
- **Recommendation logic:** Fills a PA 2.2 gap in SWE.1 — the existing SWE1 L2 question (SWE1_L2_07) only covers PA 2.1 planning. Recommend a CM-controlled requirements repository with baseline/status workflow (cf. SWE4_L2_07 pattern applied to requirements).

### `SWE1_L3_12` · Level L3 (Established) · `GP 3.1.1, GP 3.1.2`

**Base practice:** GP 3.1.1, GP 3.1.2 — Standard process & required competencies (SWE.1)

**Question:** Does the organisation maintain a standard requirements-engineering process (templates, tailoring guideline) and a defined role/competency description for the requirements-engineer role?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Documented standard RE process + tailoring guideline + role/competency description, maintained and referenced by projects | 0 |
| B | Standard process exists, but role/competency description is missing | 2 |
| C | A requirements template exists informally, not maintained centrally | 3 |
| D | Each project defines its own RE approach independently | 4 |
| E | No organisational standard or role description exists | 5 |

- **Identifies:** No organisation-wide standard for requirements-engineering methodology/roles
- **Stakeholders:** ASR, PM, SA
- **Recommendation logic:** SWE.1 had no L3 question in the original 42 or in Batch 1 — this is the sole remaining organisational-maturity gap for the process. PA 3.1 check, paralleling SWE2_L3_10's pattern for the architecture role. Recommend establishing an RE process template + role description at Process Group level.

---

## SWE.2 — Software Architectural Design

### `SWE2_L1_01` · Level L1 (Performed) · `SWE.2.BP1`

**Base practice:** SWE.2.BP1 — Specify static aspects of architecture

**Question:** How is the static structure of the SW architecture documented?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Hierarchical component model with explicit interfaces, in a modelling tool (UML/SysML/EA) | 0 |
| B | Block diagrams in modelling tool, no interface model | 2 |
| C | PowerPoint diagrams | 3 |
| D | Textual description only | 4 |
| E | Not documented | 5 |

- **Identifies:** Missing decomposition / structural views
- **Stakeholders:** SA
- **Recommendation logic:** Recommend a model-based architecture in EA/Cameo; flag tool break to traceability.

### `SWE2_L1_02` · Level L1 (Performed) · `SWE.2.BP2`

**Base practice:** SWE.2.BP2 — Specify dynamic aspects (timing, sequences, state)

**Question:** How are dynamic aspects (timing, sequencing, state) specified for the architecture?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Sequence + state diagrams + timing budgets per component | 0 |
| B | Sequence diagrams only | 2 |
| C | Narrative timing notes | 3 |
| D | Implicit, decided during coding | 4 |
| E | Not specified | 5 |

- **Identifies:** Hidden timing/concurrency defects
- **Stakeholders:** SA, SD
- **Recommendation logic:** Recommend timing-budget table; pair with SWE.5 integration tests.

### `SWE2_L1_03` · Level L1 (Performed) · `SWE.2.BP3`

**Base practice:** SWE.2.BP3 — Analyse architecture, justify chosen design (PAM 4.0 replaces former "evaluate alternatives" BP)

**Question:** How is the chosen architecture justified against alternatives and quality criteria (modularity, reliability, security)?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Documented trade-off analysis with rationale recorded per decision | 0 |
| B | Decision log with brief rationale | 2 |
| C | Verbal discussion in design review | 3 |
| D | Not justified, "as-is" | 4 |
| E | Decision-maker unknown | 5 |

- **Identifies:** Unjustified architecture, hidden trade-offs
- **Stakeholders:** SA, ASR
- **Recommendation logic:** High signal: recommend architecture-decision-record (ADR) practice.

### `SWE2_L1_04` · Level L1 (Performed) · `SWE.2.BP3`

**Base practice:** SWE.2.BP3 — interfaces & resource consumption

**Question:** How are interfaces and resource-consumption objectives (RAM/ROM/CPU/bandwidth) defined for SW components?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Each interface fully typed; RAM/ROM/CPU budgets per component | 0 |
| B | Interfaces typed; no resource budgets | 2 |
| C | Resource budgets only at SW level (not per component) | 3 |
| D | Defined only when problems arise | 4 |
| E | Not defined | 5 |

- **Identifies:** Interface ambiguity, resource overruns at HIL/qualification
- **Stakeholders:** SA, SD
- **Recommendation logic:** Recommend interface contracts + per-component budgets; verify with static analysis (SWE.4).

### `SWE2_L1_05` · Level L1 (Performed) · `SWE.2.BP4`

**Base practice:** SWE.2.BP4 — Consistency & bidirectional traceability (SW-req ↔ SW-arch)

**Question:** How is bidirectional traceability maintained between SW requirements and architectural elements?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Tool-enforced (allocation column / OSLC link) and reviewed each baseline | 0 |
| B | Maintained but not periodically audited | 2 |
| C | Manual matrix in spreadsheet | 3 |
| D | Allocation is implicit | 4 |
| E | No traceability | 5 |

- **Identifies:** Architecture/requirement drift
- **Stakeholders:** SA, QA, ASR
- **Recommendation logic:** Recommend OSLC-style linking; tie to SWE.1 traceability question to detect compounded weakness.

### `SWE2_L1_06` · Level L1 (Performed) · `SWE.2.BP5`

**Base practice:** SWE.2.BP5 — Communicate agreed architecture

**Question:** How is the agreed architecture communicated and made available to development and test teams?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Published in the team wiki + walk-through workshop with attendance log | 0 |
| B | Published in wiki only | 2 |
| C | Sent by e-mail | 3 |
| D | Available on request | 4 |
| E | Not communicated | 5 |

- **Identifies:** Architecture not internalised by team
- **Stakeholders:** SA, TL
- **Recommendation logic:** Recommend onboarding workshop + searchable architecture site.

### `SWE2_L2_07` · Level L2 (Managed) · `GP 2.2.1, GP 2.2.4`

**Base practice:** GP 2.2.1, GP 2.2.4 — Work-product requirements & review for architecture artefacts

**Question:** How are architecture work products (model, ADRs, interface specs) reviewed and approved?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Defined review checklist + approver role + review record per baseline | 0 |
| B | Review checklist but no approver role | 2 |
| C | Reviews held without checklist | 3 |
| D | Reviews held only when issues escalate | 4 |
| E | No reviews | 5 |

- **Identifies:** Architecture artefacts not reviewed against criteria
- **Stakeholders:** QA, ASR
- **Recommendation logic:** Indicates PA 2.2 weakness; recommend SUP.1-style work-product review template.

### `SWE2_L2_08` · Level L2 (Managed) · `GP 2.1.3, GP 2.1.4`

**Base practice:** GP 2.1.3, GP 2.1.4 — Resource needs & qualification (SWE.2)

**Question:** How is the competency of software architects (modelling method/tool skills) and the availability of architecture tooling (e.g., EA/Cameo licences) ensured?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Defined competency requirement, training/mentoring plan, and licence/tool availability tracked | 0 |
| B | Training available but not tracked; tool availability assumed | 2 |
| C | New architects learn on the job, no formal plan | 3 |
| D | Competency/tooling addressed only when a problem arises | 4 |
| E | No defined approach | 5 |

- **Identifies:** Architects not trained/qualified on modelling method or tool; unavailable licences
- **Stakeholders:** SA, TL, PM
- **Recommendation logic:** Fills the PA 2.1 "persons prepared for their responsibilities" achievement (GP 2.1.4), absent everywhere else in the bank; recommend a role-based training plan and licence-tracking process.

### `SWE2_L2_09` · Level L2 (Managed) · `GP 2.1.6`

**Base practice:** GP 2.1.6 — Manage interfaces between involved parties (SWE.2)

**Question:** When the software architecture changes after initial communication, how are affected detailed-design and integration teams notified and re-aligned?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Change-notification mechanism with defined recipients and acknowledgement tracking | 0 |
| B | Notification sent, but acknowledgement not tracked | 2 |
| C | Announced only in the next regular meeting | 3 |
| D | Discovered by affected teams when inconsistencies appear | 4 |
| E | No mechanism | 5 |

- **Identifies:** Architecture changes not propagated to detailed-design / integration teams
- **Stakeholders:** SA, TL, PM
- **Recommendation logic:** Distinct from the one-time communication event in SWE2_L1_06 — this targets ongoing change coordination once the architecture evolves. Recommend an architecture change board, mirroring SWE5_L2_07's ICB pattern.

### `SWE2_L2_11` · Level L2 (Managed) · `GP 2.1.1, GP 2.1.2`

**Base practice:** GP 2.1.1, GP 2.1.2 — Strategy & planning for SWE.2

**Question:** How is the SWE.2 architecture design activity planned and monitored at project level (objectives, milestones, schedule)?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Documented architecture design plan with objectives/milestones, reviewed and adjusted regularly | 0 |
| B | Plan exists but not actively monitored/adjusted | 2 |
| C | Milestones exist only in the overall project schedule, not architecture-specific | 3 |
| D | Planned ad-hoc per sprint | 4 |
| E | No plan for the architecture design activity | 5 |

- **Identifies:** Architecture design activity not planned against objectives/milestones
- **Stakeholders:** PM, SA
- **Recommendation logic:** Fills the PA 2.1 "strategy and planning" gap for SWE.2 — existing SWE2 L2 questions cover competency (SWE2_L2_08), interface/change coordination (SWE2_L2_09), and work-product review (SWE2_L2_07), but not planning of the design activity itself. Mirrors the SWE1_L2_07 pattern, applied to the architecture process.

### `SWE2_L3_10` · Level L3 (Established) · `GP 3.1.2, GP 3.1.3`

**Base practice:** GP 3.1.2, GP 3.1.3 — Required competencies & resources for the standard process (SWE.2)

**Question:** Does the organisation maintain a defined role description (required competencies, responsibilities) and standard tooling/infrastructure for the software architect role?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Documented role description and standard tooling maintained and referenced by projects | 0 |
| B | Role description exists but tooling/infrastructure not standardised | 2 |
| C | Informal, unwritten expectations for the role | 3 |
| D | Role description exists only for other roles (not architect) | 4 |
| E | No role description or standard infrastructure defined | 5 |

- **Identifies:** No organisation-level role/competency definition for the architecture role
- **Stakeholders:** ASR, PM, SA
- **Recommendation logic:** PA 3.1 organisational-maturity check — approximated here from a single respondent's session, per the documented tool limitation (Section 7.4 note in concepts doc); recommend establishing a role-description template at Process Group level.

---

## SWE.3 — Software Detailed Design and Unit Construction

### `SWE3_L1_01` · Level L1 (Performed) · `SWE.3.BP1`

**Base practice:** SWE.3.BP1 — Specify static aspects of detailed design

**Question:** How is the static detailed design of software units captured?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Class/data structure model in tool, generated from architecture | 0 |
| B | Diagrams in modelling tool, manually maintained | 2 |
| C | Text-and-code-comments only | 3 |
| D | Comments in source code | 4 |
| E | No detailed design | 5 |

- **Identifies:** Skipping detailed design, "code-is-design" antipattern
- **Stakeholders:** SA, SD
- **Recommendation logic:** Recommend keeping design synchronised via code-from-model or model-from-code.

### `SWE3_L1_02` · Level L1 (Performed) · `SWE.3.BP2`

**Base practice:** SWE.3.BP2 — Specify dynamic aspects of detailed design

**Question:** How are state machines, control flows, and unit interactions described?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | State/sequence diagrams per non-trivial unit | 0 |
| B | Diagrams only for safety-critical units | 2 |
| C | Narrative description | 3 |
| D | Discovered during coding | 4 |
| E | Not described | 5 |

- **Identifies:** Hidden control-flow / state defects
- **Stakeholders:** SD, SA
- **Recommendation logic:** Recommend state-chart coverage for safety-critical paths.

### `SWE3_L1_03` · Level L1 (Performed) · `SWE.3.BP3`

**Base practice:** SWE.3.BP3 — Develop software units (coding standard adherence)

**Question:** How are coding standards (e.g., MISRA C/C++, AUTOSAR C++14) enforced during unit construction?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Pre-commit check + CI gate blocks merges on standard violations | 0 |
| B | CI gate runs but does not block merges | 2 |
| C | Periodic audit by QA | 3 |
| D | Standard exists but is not enforced | 4 |
| E | No coding standard adopted | 5 |

- **Identifies:** Coding-standard violations, MISRA gaps
- **Stakeholders:** SD, QA
- **Recommendation logic:** High signal: recommend Axivion/Polyspace/Coverity gate; flag SWE.4 static-analysis question for re-check.

### `SWE3_L1_04` · Level L1 (Performed) · `SWE.3.BP4`

**Base practice:** SWE.3.BP4 — Consistency & bidirectional traceability (SW-req ↔ arch ↔ detailed design ↔ units)

**Question:** What is the state of traceability from architecture → detailed design → source units?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | End-to-end tool-enforced, audited each release | 0 |
| B | Forward links complete; reverse links partial | 2 |
| C | Spreadsheet only | 3 |
| D | Traceability stops at design level | 4 |
| E | No links | 5 |

- **Identifies:** Multi-hop traceability gap
- **Stakeholders:** SA, QA, ASR
- **Recommendation logic:** Strongest predictor of CL2 failure across SWE.3; recommend OSLC link consolidation.

### `SWE3_L1_05` · Level L1 (Performed) · `SWE.3.BP5`

**Base practice:** SWE.3.BP5 — Communicate agreed detailed design and units

**Question:** How are agreed detailed design and developed units made available to peers and testers?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Reviewed pull requests + design documented in shared repo | 0 |
| B | Code committed, design in shared repo | 2 |
| C | Code only, design private to developer | 3 |
| D | Code on local branches, no design | 4 |
| E | Knowledge held by one developer | 5 |

- **Identifies:** Knowledge silo, single-point-of-failure
- **Stakeholders:** SD, TL
- **Recommendation logic:** Recommend mandatory peer review and shared design index.

### `SWE3_L2_06` · Level L2 (Managed) · `GP 2.1.5`

**Base practice:** GP 2.1.5 — Monitor & adjust process (defect/rework rates per unit)

**Question:** How is the SWE.3 process monitored at project level (e.g., rework, defect density per unit)?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Defect-density and rework metrics tracked weekly with thresholds | 0 |
| B | Metrics tracked monthly, no thresholds | 2 |
| C | Metrics gathered only for assessments | 3 |
| D | No monitoring beyond burndown | 4 |
| E | Not monitored | 5 |

- **Identifies:** No control loop for code quality
- **Stakeholders:** TL, QA, PM
- **Recommendation logic:** PA 2.1 weakness; recommend defect-density dashboard and threshold-based escalation.

### `SWE3_L2_08` · Level L2 (Managed) · `GP 2.2.2, GP 2.2.3`

**Base practice:** GP 2.2.2, GP 2.2.3 — Storage and control of work products (source code & detailed design)

**Question:** How are source code and detailed-design work products identified, versioned, and controlled during development?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Version-controlled with branching/baseline policy and a defined status model (e.g., Under Work/Reviewed/Released) | 0 |
| B | Version-controlled, but no defined status model | 2 |
| C | Version-controlled only for source code, not detailed design | 3 |
| D | Ad-hoc use of version control, no policy | 4 |
| E | Not under version/configuration control | 5 |

- **Identifies:** Source code / detailed design not under proper configuration control
- **Stakeholders:** QA, SD, ASR
- **Recommendation logic:** Distinct from SWE3_L2_06 (defect/rework monitoring, GP 2.1.5) — this fills the PA 2.2 work-product-control gap for SWE.3. Recommend a CM branching/baseline policy covering both code and design artefacts.

### `SWE3_L2_09` · Level L2 (Managed) · `GP 2.1.1, GP 2.1.2`

**Base practice:** GP 2.1.1, GP 2.1.2 — Strategy & planning for SWE.3

**Question:** How is the SWE.3 detailed design and unit construction activity planned (staffing, schedule, objectives per component)?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Documented plan with per-component staffing/schedule, objectives tracked and adjusted | 0 |
| B | Plan exists but not tracked against actuals | 2 |
| C | Only covered by the general sprint backlog, no dedicated plan | 3 |
| D | Planned informally by the team lead | 4 |
| E | No planning for the detailed design/construction activity | 5 |

- **Identifies:** Detailed design & unit construction activity not planned against objectives/staffing
- **Stakeholders:** PM, TL, SD
- **Recommendation logic:** Fills the PA 2.1 "strategy and planning" gap for SWE.3 — existing SWE3 L2 questions cover monitoring (SWE3_L2_06, GP 2.1.5) and CM control (SWE3_L2_08, GP 2.2), but not upfront planning of the activity itself.

### `SWE3_L3_07` · Level L3 (Established) · `GP 3.1.1, GP 3.1.4`

**Base practice:** GP 3.1.1, GP 3.1.4 — Standard process & tailoring guidelines

**Question:** How is the organisation’s standard SWE.3 process tailored for this project?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Tailoring documented against tailoring guidelines, reviewed by Process Group | 0 |
| B | Tailoring documented, not reviewed | 2 |
| C | Project follows standard process verbatim, no tailoring | 3 |
| D | Tailoring done informally | 4 |
| E | No standard process exists | 5 |

- **Identifies:** Project-specific drift from organisational standard
- **Stakeholders:** ASR, QA, PM
- **Recommendation logic:** Note: option C is mid-risk because lack of tailoring often hides cargo-cult adoption; recommend formal tailoring record.

---

## SWE.4 — Software Unit Verification

### `SWE4_L1_01` · Level L1 (Performed) · `SWE.4.BP1`

**Base practice:** SWE.4.BP1 — Specify unit-verification measures (tactic)

**Question:** How are unit-verification measures (test cases, static analysis, coverage goals) specified?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Documented per component, derived from detailed design and non-functional reqs | 0 |
| B | Documented but not derived from non-functional reqs | 2 |
| C | Test cases only, no static-analysis measures | 3 |
| D | Specified ad-hoc | 4 |
| E | Not specified | 5 |

- **Identifies:** Missing verification tactic
- **Stakeholders:** TE, SD
- **Recommendation logic:** Recommend a unit-verification specification template with derivation columns.

### `SWE4_L1_02` · Level L1 (Performed) · `SWE.4.BP2`

**Base practice:** SWE.4.BP2 — Select verification measures incl. regression

**Question:** How are verification measures selected per release, including regression?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Selection rules documented and applied per release; regression set auto-derived from change-impact | 0 |
| B | Regression decided manually each release | 2 |
| C | Always run all unit tests | 2 |
| D | Regression decided only when defects appear | 4 |
| E | No selection mechanism | 5 |

- **Identifies:** Insufficient regression coverage
- **Stakeholders:** TE
- **Recommendation logic:** High signal for late-stage defects; recommend change-impact-driven regression.

### `SWE4_L1_03` · Level L1 (Performed) · `SWE.4.BP3`

**Base practice:** SWE.4.BP3 — Verify (static + dynamic)

**Question:** How is static analysis performed on software units?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Tool integrated in CI; zero high-severity findings policy | 0 |
| B | Tool integrated in CI; findings tracked but not blocking | 2 |
| C | Manual code reviews only | 3 |
| D | Static analysis runs only before milestones | 4 |
| E | Not performed | 5 |

- **Identifies:** Weak static analysis
- **Stakeholders:** SD, QA
- **Recommendation logic:** Reinforces SWE3_L1_03; recommend severity-based blocking gate.

### `SWE4_L1_04` · Level L1 (Performed) · `SWE.4.BP3`

**Base practice:** SWE.4.BP3 — Test SW units & record results (coverage)

**Question:** What unit-test coverage criteria are applied for non-safety code?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Statement + branch coverage with documented threshold (e.g., ≥ 90 % branch) | 0 |
| B | Statement coverage threshold only | 2 |
| C | Coverage measured but no threshold | 3 |
| D | Coverage measured ad-hoc | 4 |
| E | Not measured | 5 |

- **Identifies:** Inadequate structural coverage
- **Stakeholders:** TE, SD
- **Recommendation logic:** Recommend MC/DC for ASIL B+ paths; align thresholds with ISO 26262 (referenced).

### `SWE4_L1_05` · Level L1 (Performed) · `SWE.4.BP4`

**Base practice:** SWE.4.BP4 — Bidirectional traceability between units, criteria, results

**Question:** How are unit-test results linked to verification criteria and units?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Tool-enforced bidirectional links; audited each release | 0 |
| B | Manual matrix maintained | 2 |
| C | Links exist for failed tests only | 3 |
| D | Linked only when assessor asks | 4 |
| E | Not linked | 5 |

- **Identifies:** Test-result orphaning
- **Stakeholders:** TE, QA, ASR
- **Recommendation logic:** Recommend test-management tool integration (e.g., qTest/Jama/Polarion).

### `SWE4_L1_08` · Level L1 (Performed) · `SWE.4.BP5`

**Base practice:** SWE.4.BP5 — Summarize and communicate results

**Question:** How are software unit-verification results (pass/fail, coverage, static-analysis findings) summarised and communicated to affected parties?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Automated summary report generated per build/release and distributed to affected parties | 0 |
| B | Summary report generated but only on request | 2 |
| C | Results visible only inside the test-management tool, not actively communicated | 3 |
| D | Communicated verbally / informally | 4 |
| E | Not summarised or communicated | 5 |

- **Identifies:** Unit-verification results not summarised/communicated to affected parties
- **Stakeholders:** SD, TE, TL
- **Recommendation logic:** Closes a full outcome gap — BP5/Outcome 5 was previously unassessed for SWE.4 across all 42 questions. Recommend a build-level unit-verification summary report distributed to development and QA.

### `SWE4_L2_06` · Level L2 (Managed) · `GP 2.1.6, GP 2.1.7`

**Base practice:** GP 2.1.6, GP 2.1.7 — Resources & stakeholder management for SWE.4

**Question:** How is access to test infrastructure (HIL/SIL, test benches, target boards) planned and assured for unit verification?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Infrastructure capacity planned per release; bottleneck escalation defined | 0 |
| B | Plan exists but no escalation path | 2 |
| C | Access requested per sprint | 3 |
| D | Access negotiated when needed | 4 |
| E | Frequent blocking due to unavailable HW | 5 |

- **Identifies:** Under-resourced verification, late access to HW/test bench
- **Stakeholders:** PM, TL, TE
- **Recommendation logic:** Strongest "release-phase" predictor; recommend resource calendar + escalation.

### `SWE4_L2_07` · Level L2 (Managed) · `GP 2.2.3, GP 2.2.4`

**Base practice:** GP 2.2.3, GP 2.2.4 — Work-product control & review of unit-verification reports

**Question:** How are unit-verification reports stored, versioned, and reviewed?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Versioned in CM with status workflow + reviewer sign-off | 0 |
| B | Versioned only | 2 |
| C | Stored on shared drive, no versioning | 3 |
| D | Stored locally | 4 |
| E | Not formally stored | 5 |

- **Identifies:** Reports not under configuration control
- **Stakeholders:** QA
- **Recommendation logic:** Recommend CM-controlled report storage (referenced SUP.8).

### `SWE4_L3_09` · Level L3 (Established) · `GP 3.1.1, GP 3.1.4`

**Base practice:** GP 3.1.1, GP 3.1.4 — Standard process & monitoring (SWE.4)

**Question:** Is there an organisation-wide standard for unit-verification methods/tooling (static-analysis rulesets, coverage thresholds), and is its effectiveness monitored?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Standard method/tooling defined, tailoring guideline available, effectiveness monitored and fed back | 0 |
| B | Standard defined, but effectiveness not monitored | 2 |
| C | Each project chooses its own tooling/thresholds independently | 3 |
| D | Standard exists informally, not documented | 4 |
| E | No organisational standard for unit verification | 5 |

- **Identifies:** Unit-verification approach/tooling not standardised or monitored across projects
- **Stakeholders:** ASR, QA, PM
- **Recommendation logic:** SWE.4 previously had no L3 question; parallels SWE6_L3_07's feedback-loop pattern applied to unit verification. Recommend a Process Group review of unit-verification effectiveness metrics.

---

## SWE.5 — Software Component Verification and Integration Verification

### `SWE5_L1_01` · Level L1 (Performed) · `SWE.5.BP1`

**Base practice:** SWE.5.BP1 — Specify integration-verification measures

**Question:** How are integration-verification measures defined for the integrated software?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Per-component and per-interface measures derived from architecture | 0 |
| B | Per-component only | 2 |
| C | End-to-end tests only | 3 |
| D | Defined as needed | 4 |
| E | Not defined | 5 |

- **Identifies:** Missing integration-verification scope
- **Stakeholders:** TE, SA
- **Recommendation logic:** Recommend interface-driven integration-verification specs.

### `SWE5_L1_02` · Level L1 (Performed) · `SWE.5.BP2`

**Base practice:** SWE.5.BP2 — Specify component-behaviour verification measures (PAM 4.0 novelty)

**Question:** How is software-component behaviour verified before integration?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Component contract tests run against published interfaces in CI | 0 |
| B | Component tests exist but run manually | 2 |
| C | Verified only as part of integration | 3 |
| D | Verified only at qualification | 4 |
| E | Not verified at component level | 5 |

- **Identifies:** Component-level black-box gaps
- **Stakeholders:** TE, SA
- **Recommendation logic:** New PAM 4.0 expectation; high signal of legacy 3.1 process.

### `SWE5_L1_03` · Level L1 (Performed) · `SWE.5.BP3`

**Base practice:** SWE.5.BP3 — Select verification measures incl. regression

**Question:** How are integration-test cases selected per release (including regression)?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Selection rules + change-impact-driven regression set documented | 0 |
| B | Regression rules only | 2 |
| C | "Run everything" | 2 |
| D | Selected ad-hoc | 4 |
| E | No selection criteria | 5 |

- **Identifies:** Selection criteria absent
- **Stakeholders:** TE
- **Recommendation logic:** Recommend traceable selection rules linked to release scope.

### `SWE5_L1_04` · Level L1 (Performed) · `SWE.5.BP4`

**Base practice:** SWE.5.BP4 — Integrate elements & perform integration verification

**Question:** How are software elements integrated and verified?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Continuous integration with stepwise integration plan and per-step verification | 0 |
| B | Stepwise integration but verification batched | 2 |
| C | Daily integration without integration plan | 3 |
| D | Big-bang integration at end of sprint | 4 |
| E | Big-bang integration at end of release | 5 |

- **Identifies:** Big-bang integration risk
- **Stakeholders:** SD, TE, SA
- **Recommendation logic:** High signal of late defects; recommend stepwise integration plan with CI.

### `SWE5_L1_05` · Level L1 (Performed) · `SWE.5.BP5`

**Base practice:** SWE.5.BP5 — Perform component verification & record

**Question:** How are component-verification and integration-verification results recorded?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Recorded automatically in test-management tool with status, evidence, environment metadata | 0 |
| B | Recorded in test tool, no environment metadata | 2 |
| C | Captured in spreadsheets | 3 |
| D | Captured in e-mail/chat | 4 |
| E | Not recorded | 5 |

- **Identifies:** Result records missing
- **Stakeholders:** QA, TE
- **Recommendation logic:** Recommend tool-based recording with environment fingerprint.

### `SWE5_L1_06` · Level L1 (Performed) · `SWE.5.BP6`

**Base practice:** SWE.5.BP6 — Consistency & bidirectional traceability (arch / detailed design ↔ verification measures ↔ results)

**Question:** What is the state of bidirectional traceability between architecture/design, integration verification measures, and results?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Tool-enforced bidirectional links with periodic audits | 0 |
| B | Forward only | 2 |
| C | Spreadsheet matrix | 3 |
| D | Implicit | 4 |
| E | None | 5 |

- **Identifies:** Verification-result orphaning at integration
- **Stakeholders:** QA, ASR
- **Recommendation logic:** Compose with SWE2_L1_05 for compounded signal.

### `SWE5_L1_08` · Level L1 (Performed) · `SWE.5.BP7`

**Base practice:** SWE.5.BP7 — Summarize and communicate results

**Question:** How are software component-verification and integration-verification results summarised and communicated to affected parties?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Versioned summary report per integration baseline with pass/fail overview, distributed to affected parties | 0 |
| B | Summary report exists, distributed only on request | 2 |
| C | Results visible in test tool only, not actively communicated | 3 |
| D | Communicated verbally in status meetings | 4 |
| E | Not summarised or communicated | 5 |

- **Identifies:** Component/integration verification results not summarised/communicated
- **Stakeholders:** TE, SA, PM
- **Recommendation logic:** Closes a full outcome gap — BP7/Outcome 8 was previously unassessed for SWE.5 across all 42 questions. Recommend an integration-baseline summary report as a release-readiness input to SWE.6.

### `SWE5_L2_07` · Level L2 (Managed) · `GP 2.1.4`

**Base practice:** GP 2.1.4 — Adjust process performance (interface management between SD & integration team)

**Question:** How are interface changes coordinated between development and integration teams?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Interface change board with affected-party notification SLA | 0 |
| B | E-mail notification policy in place | 2 |
| C | Notified during integration only | 3 |
| D | Discovered during failure | 4 |
| E | No coordination mechanism | 5 |

- **Identifies:** Interface miscommunication between teams
- **Stakeholders:** TL, PM
- **Recommendation logic:** PA 2.1 / GP 2.1.7 (involved-party management); recommend lightweight ICB.

### `SWE5_L2_09` · Level L2 (Managed) · `GP 2.2.2, GP 2.2.3`

**Base practice:** GP 2.2.2, GP 2.2.3 — Storage and control of work products (component/integration verification reports)

**Question:** How are component-verification and integration-verification reports stored, versioned, and controlled?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Versioned in CM with a defined status workflow and reviewer sign-off | 0 |
| B | Versioned only, no status workflow | 2 |
| C | Stored on a shared drive, no versioning | 3 |
| D | Stored locally by individual testers | 4 |
| E | Not formally stored | 5 |

- **Identifies:** Integration-verification reports not under configuration control
- **Stakeholders:** QA
- **Recommendation logic:** Fills the PA 2.2 gap for SWE.5 — the existing SWE5 GP question (SWE5_L2_07) covers only PA 2.1 interface coordination. Mirrors the SWE4_L2_07 pattern applied to the integration-verification artefact set.

### `SWE5_L3_10` · Level L3 (Established) · `GP 3.1.1`

**Base practice:** GP 3.1.1 — Standard process (integration strategy)

**Question:** Does the organisation define a standard integration strategy (e.g., stepwise vs. continuous integration, environments to be used) that projects tailor from?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Documented standard integration strategy with tailoring guideline, applied and reviewed | 0 |
| B | Standard exists but tailoring is undocumented | 2 |
| C | Each project defines its own integration strategy independently | 3 |
| D | Informal convention, not documented | 4 |
| E | No organisational standard | 5 |

- **Identifies:** No organisation-wide standard for integration approach
- **Stakeholders:** ASR, SA, PM
- **Recommendation logic:** SWE.5 previously had no L3 question; PA 3.1 organisational-maturity check. Recommend a Process Group-maintained integration-strategy template.

---

## SWE.6 — Software Verification

### `SWE6_L1_01` · Level L1 (Performed) · `SWE.6.BP1`

**Base practice:** SWE.6.BP1 — Specify verification measures vs. SW requirements

**Question:** How are software-verification measures derived from SW requirements?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Each SW requirement has at least one verification measure recorded with technique justification | 0 |
| B | Coverage exists but technique not justified | 2 |
| C | Coverage is partial | 3 |
| D | Tests written from intuition | 4 |
| E | Not derived from SW requirements | 5 |

- **Identifies:** Test cases not derived from SW requirements
- **Stakeholders:** TE
- **Recommendation logic:** Recommend req-to-test allocation report at each baseline.

### `SWE6_L1_02` · Level L1 (Performed) · `SWE.6.BP2`

**Base practice:** SWE.6.BP2 — Select verification measures incl. regression (release scope)

**Question:** How are SWE.6 verification measures selected for the release, including regression?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Documented selection per release with risk-based regression set | 0 |
| B | Selection per release without risk weighting | 2 |
| C | Always full re-run | 2 |
| D | Selected verbally per stand-up | 4 |
| E | No selection process | 5 |

- **Identifies:** Regression policy weak at qualification
- **Stakeholders:** TE, PM
- **Recommendation logic:** High signal pre-release; flag if release phase = late.

### `SWE6_L1_03` · Level L1 (Performed) · `SWE.6.BP3`

**Base practice:** SWE.6.BP3 — Verify integrated SW & record (qualification environment)

**Question:** What environment is used for SWE.6 qualification verification?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Representative target HW (HIL/real ECU) with calibrated parameters | 0 |
| B | HIL only | 2 |
| C | SIL/MIL with HW abstraction | 3 |
| D | PC simulation | 4 |
| E | Developer machine | 5 |

- **Identifies:** Wrong target / non-representative env.
- **Stakeholders:** TE, QA
- **Recommendation logic:** Recommend escalation to HIL for safety-critical functions.

### `SWE6_L1_04` · Level L1 (Performed) · `SWE.6.BP4`

**Base practice:** SWE.6.BP4 — Consistency & bidirectional traceability (SW reqs ↔ test specs ↔ results)

**Question:** How is bidirectional traceability maintained between SW requirements, qualification test specs, and results?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Tool-enforced and audited each release | 0 |
| B | Maintained but not audited | 2 |
| C | Spreadsheet | 3 |
| D | Manual when needed | 4 |
| E | None | 5 |

- **Identifies:** Final-stage traceability gap
- **Stakeholders:** QA, ASR
- **Recommendation logic:** Compose with SWE1_L1_05; if both high → critical traceability red flag.

### `SWE6_L1_05` · Level L1 (Performed) · `SWE.6.BP5`

**Base practice:** SWE.6.BP5 — Summarise & communicate results

**Question:** How are qualification-test results summarised and communicated to affected parties?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Versioned test-summary report per release with go/no-go criteria | 0 |
| B | Report exists but no go/no-go criteria | 2 |
| C | Slide summary at release meeting | 3 |
| D | Verbal summary | 4 |
| E | Not communicated | 5 |

- **Identifies:** Defect leakage / no test summary
- **Stakeholders:** QA, PM
- **Recommendation logic:** Recommend templated test summary tied to release approval.

### `SWE6_L2_06` · Level L2 (Managed) · `GP 2.2.2`

**Base practice:** GP 2.2.2 — Work-product requirements (defect management)

**Question:** How are qualification-test defects managed and triaged?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Defects in tracker with severity, owner, SLA, root-cause field; weekly triage | 0 |
| B | Tracker used; no triage cadence | 2 |
| C | Defects in spreadsheet | 3 |
| D | Verbally tracked | 4 |
| E | No defect tracking | 5 |

- **Identifies:** Defect process weak at qualification
- **Stakeholders:** QA, TE
- **Recommendation logic:** Reference SUP.9 (out of scope); recommend root-cause field.

### `SWE6_L2_08` · Level L2 (Managed) · `GP 2.1.1, GP 2.1.2, GP 2.1.3`

**Base practice:** GP 2.1.1, GP 2.1.2, GP 2.1.3 — Strategy, planning and resource readiness for SWE.6

**Question:** How is the SWE.6 qualification-verification activity planned and resourced ahead of a release (schedule, staffing, target-environment availability)?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Documented plan with milestones, staffing, and environment booking confirmed ahead of release | 0 |
| B | Plan exists but staffing/environment not confirmed in advance | 2 |
| C | Planned informally per release, no documented milestones | 3 |
| D | Planned reactively once development is "done" | 4 |
| E | No planning for qualification verification | 5 |

- **Identifies:** Qualification-verification activity not planned/resourced ahead of release
- **Stakeholders:** PM, TE, TL
- **Recommendation logic:** Fills the PA 2.1 gap for SWE.6 — the existing SWE6 GP questions cover only PA 2.2 (defect management, SWE6_L2_06) and PA 3.2 (feedback loop, SWE6_L3_07), never PA 2.1 planning. Recommend a release-readiness checklist including qualification-environment booking (cf. SWE4_L2_06 pattern applied to the qualification stage).

### `SWE6_L3_07` · Level L3 (Established) · `GP 3.2.4`

**Base practice:** GP 3.2.4 — Monitor performance of defined process (information, not data)

**Question:** How is information from SWE.6 fed back into the organisational standard process?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Lessons-learned + KPIs reported to Process Group; standard process updated | 0 |
| B | Lessons-learned written, no link to standard process | 2 |
| C | Discussed in retro only | 3 |
| D | Captured in private notes | 4 |
| E | No feedback loop | 5 |

- **Identifies:** No process-improvement feedback loop
- **Stakeholders:** ASR, QA, PM
- **Recommendation logic:** PA 3.2 weakness; recommend a quarterly Process Group review channel.

### `SWE6_L3_09` · Level L3 (Established) · `GP 3.1.1`

**Base practice:** GP 3.1.1 — Standard process (qualification-test strategy)

**Question:** Does the organisation maintain a standard qualification-test methodology/template (e.g., technique-selection guideline, standard test-environment setup) that projects tailor from?

| Option | Answer | Weight |
|:---:|---|:---:|
| A | Documented standard methodology/template with tailoring guideline, applied and reviewed across projects | 0 |
| B | Standard exists but the tailoring guideline is missing | 2 |
| C | Each project defines its own qualification-test methodology independently | 3 |
| D | Informal convention, not documented | 4 |
| E | No organisational standard | 5 |

- **Identifies:** No organisation-wide standard qualification-test methodology
- **Stakeholders:** ASR, TE, PM
- **Recommendation logic:** Distinct from SWE6_L3_07 (GP 3.2.4 — monitoring/feedback loop of the already-deployed process) — this addresses GP 3.1.1, the prior step of establishing a standard process in the first place. Closes the last PA 3.1 gap for SWE.6, paralleling SWE4_L3_09/SWE5_L3_10.

---

