# Automotive SPICE® PAM v4.0 — Curated Reference for the Thesis

> Source: `Automotive-SPICE-PAM-v40.pdf` (VDA Working Group 13, v4.0, 2023-11-29).
> This file keeps only the material relevant to the thesis (SWE.1–SWE.6, the measurement
> framework at capability levels 0–3, and general PRM/PAM concepts). Full process groups
> not touched by the tool (ACQ, SPL, SYS details, VAL, MLE, HWE, most of SUP/MAN/PIM/REU,
> capability levels 4–5, and Annex A/B/D in full) are deliberately left out or summarized in
> one line — go back to the original PDF only if a specific need arises for those.
>
> Use this as the primary source for: Ch.2 Background (ASPICE fundamentals), Ch.4.4/4.6
> Weakness Classifier & question bank traceability (base_practice_id), and any place the
> thesis needs to quote/paraphrase the standard's own definitions.

---

## 1. Scope and Purpose of the PAM/PRM (Section 1.1, 3)

Process assessment is a disciplined evaluation of an organizational unit's processes against
a process assessment model (PAM). The Automotive SPICE PAM is intended for conformant
assessments of process capability in embedded automotive systems development, developed
per ISO/IEC 33004:2015.

Automotive SPICE has its own **Process Reference Model (PRM)**, based on and tailored from
generic reference models for the automotive industry. The PRM is incorporated into the PAM
and used jointly when performing an assessment.

The concept of **process capability determination** rests on a **two-dimensional framework**:

- **Process dimension** — the processes defined in the PRM (e.g., SWE.1–SWE.6), each with a
  purpose statement and a list of process outcomes.
- **Capability dimension** — capability levels (0–5), further subdivided into **process
  attributes (PA)**, which provide the measurable characteristics of process capability.

The PAM selects processes from the PRM and supplements them with **indicators** (base
practices, generic practices, information items) that support collecting objective evidence
to rate a process along the capability dimension.

```
Measurement framework                 Process assessment model (Automotive SPICE)
  - Capability levels                   - Process capability indicators
  - Process attributes                  - Process performance indicators
  - Rating (scale, method, aggregation)
  - Process capability level model

                    ↑
Process reference model (Automotive SPICE)
  - Domain and scopes
  - Process purposes
  - Process outcomes
```
*(Figure 1 — Process assessment model relationship, p.14)*

### Three process categories (Section 3.1)

- **Primary life cycle processes** — ACQ, SPL, SYS, VAL, **SWE**, MLE, HWE
- **Supporting life cycle processes** — SUP
- **Organizational life cycle processes** — MAN, PIM, REU

The **Software Engineering process group (SWE)** — the group this thesis's question bank is
built on — "consists of processes addressing the management of software requirements
derived from the system requirements, the development of the corresponding software
architecture and design as well as the implementation, integration and verification of the
software": SWE.1–SWE.6 (Table 7, p.16).

---

## 2. Relevant Terminology (subset of Table 1, p.9–11)

| Term | Description |
|---|---|
| **Activity** | Execution of a task by a stakeholder or an involved party. |
| **Baseline** | A defined and coherent set of read-only information, serving as input information for affected parties. |
| **Deliverable** | Any unique and verifiable product, result, or capability to perform a service that must be produced to complete a process, phase, or project. |
| **Functional requirement** | A statement that identifies what a product or process must accomplish to produce required behavior and/or results. |
| **Measure** | An activity to achieve a certain intent (i.e., "a plan of action" — see Annex C.7 terminology note below). |
| **Measurement** | "The activity to find the size, quantity or degree of something." |
| **Metric** | A quantitative or qualitative measurable indicator that matches defined information needs. |
| **Project** | Endeavor with defined start and finish dates undertaken to create a product or service in accordance with specified resources and requirements. |
| **Regression verification** | Selective re-verification of elements to verify that modifications have not caused unintended effects. |
| **Risk** | The combination of the probability of occurrence and the consequences of a given future undesirable event. |
| **Software component** | *Design/implementation-oriented*: the software architecture decomposes the software into software components across hierarchical levels down to the lowest-level software components in a conceptual model. *Verification-oriented*: the implementation of a SW component under verification (source code, object files, library file, executable, or executable model). |
| **Software element** | Refers to software component or software unit. |
| **Software unit** | *Design/implementation-oriented*: the lowest-level representation of a software element, decided not to be further subdivided, part of a software component. *Verification-oriented*: an implemented SW unit under verification (source code files, or object file). |
| **Stakeholder requirements** | Any type of requirement for the stakeholders in the given context (customer, supplier-internal, legal, regulatory, statutory, industry-sector, international standards, codes of practice, etc.). |
| **Task** | A definition, but not the execution, of a coherent set of atomic actions. |
| **Verification** | Confirmation through the provision of objective evidence that an element fulfils the specified requirements. |
| **Verification measure** | Can be: test cases, measurements, calculations, simulations, reviews, analyses. Not all verification measures apply in every domain (e.g., software units generally cannot be verified by calculation or analysis). |

---

## 3. Relevant Abbreviations (subset of Table 2, p.12)

| Abbr. | Meaning |
|---|---|
| BP | Base Practice |
| GP | Generic Practice |
| GR | Generic Resource |
| PA | Process Attribute |
| PAM | Process Assessment Model |
| PRM | Process Reference Model |
| SPICE | Systems Process Improvement and Capability dEtermination |
| WP | Work Product |
| WPC | Work Product Characteristic |
| ISO/IEC | International Organization for Standardization / International Electrotechnical Commission |
| SUG | SPICE User Group |

(Domain-specific abbreviations such as CAN, ECU, PWM, RAM/ROM, MISRA, MOST, LIN, EEPROM,
etc. are HWE/system-level terms and were dropped as out of scope.)

---

## 4. The Measurement Framework (Section 3.2)

The measurement framework defines a schema enabling an assessor to determine the
**Capability Level** of a process. It is Automotive SPICE's own adaptation of ISO/IEC
33020:2019.

### 4.1 Capability Levels (Table 14, p.18–19)

| Level | Name | Description |
|---|---|---|
| **0** | Incomplete process | The process is not implemented or fails to achieve its process purpose. |
| **1** | Performed process | The implemented process achieves its process purpose. |
| **2** | Managed process | The performed process is now implemented in a managed fashion (planned, monitored, adjusted) and its work products are appropriately established, controlled, and maintained. |
| **3** | Established process | The managed process is now implemented using a defined process capable of achieving its process outcomes. |
| **4** | Predictable process | *(out of scope for this thesis — tool only covers L1–L3)* The established process now operates predictively within defined limits. |
| **5** | Innovating process | *(out of scope)* The predictable process is now continually improved to respond to organizational change. |

> **Note for the thesis:** the ASPICE Audit tool's `AspiceLevelEnum` only models **L1
> (Performed), L2 (Managed), L3 (Established)** — matching the project's own "traditional
> ASPICE levels" framing in `Architecture.md`. Levels 4–5 (Predictable / Innovating,
> quantitative process control) are explicitly a documented **future work / scope
> limitation** — cite Section 5.5–5.6 of the PAM if the thesis needs to explain why they
> were excluded.

### 4.2 Process Attributes (Table 15, p.19)

| Attribute ID | Process Attribute | Capability Level |
|---|---|---|
| PA 1.1 | Process performance | 1 |
| PA 2.1 | Process performance management | 2 |
| PA 2.2 | Work product management | 2 |
| PA 3.1 | Process definition | 3 |
| PA 3.2 | Process deployment | 3 |
| PA 4.1 | Quantitative analysis | 4 *(out of scope)* |
| PA 4.2 | Quantitative control | 4 *(out of scope)* |
| PA 5.1 | Process innovation | 5 *(out of scope)* |
| PA 5.2 | Process innovation implementation | 5 *(out of scope)* |

### 4.3 Rating Scale (Table 16–19, p.19–21)

| Rating | Meaning | % Achievement |
|---|---|---|
| N — Not achieved | Little or no evidence of achievement of the process attribute. | 0–≤15% |
| P — Partially achieved | Some evidence of an approach to, and some achievement of, the attribute; some aspects unpredictable. | >15–≤50% |
| L — Largely achieved | Systematic approach to, significant achievement; some weaknesses may exist. | >50–≤85% |
| F — Fully achieved | Complete and systematic approach, full achievement; no significant weaknesses. | >85–≤100% |

Refined scale (optional): **P−** (>15–≤32.5%), **P+** (>32.5–≤50%), **L−** (>50–≤67.5%),
**L+** (>67.5–≤85%).

> **Direct parallel to the thesis's own design:** this four/eight-point ordinal rating scale
> is conceptually the ancestor of the tool's own **0–4 answer-weight scale** and the
> **0.00–1.00 weakness-score thresholds** (`Compliant / Minor Weakness / Significant Gap /
> Critical Gap` in `Architecture.md` §5) — worth an explicit comparison in Ch.4.9 (Key
> Design Decisions) or Ch.2 (Background) to justify why the tool's own scale was chosen
> instead of directly reusing the PAM's N/P/L/F scale (continuous 0–1 score vs. ordinal
> categories; supports a regression-style bandit reward signal, which N/P/L/F does not).

### 4.4 Rating and Aggregation Methods (Section 3.2.3)

ISO/IEC 33020:2019 (adopted as-is) defines three rating methods (R1–R3), differing in
whether rating happens at process-attribute-outcome level (R1, most granular) or only at
process-attribute level (R2/R3), and whether aggregation is vertical (within one process
instance), horizontal (across instances of the same process), or two-dimensional (matrix,
across both).

### 4.5 Process Capability Level Model (Table 20, p.23)

The level achieved by a process is derived from its process-attribute ratings: as a general
rule, achieving a given level requires **Largely or Fully** achievement of the level's own
attributes and **Fully** achievement of all lower-level attributes.

| Scale | Required Attribute Ratings |
|---|---|
| Level 1 | PA 1.1: Largely or Fully |
| Level 2 | PA 1.1: Fully; PA 2.1: Largely/Fully; PA 2.2: Largely/Fully |
| Level 3 | PA 1.1, 2.1, 2.2: Fully; PA 3.1: Largely/Fully; PA 3.2: Largely/Fully |
| Level 4 *(out of scope)* | PA 1.1–3.2: Fully; PA 4.1, 4.2: Largely/Fully |
| Level 5 *(out of scope)* | PA 1.1–4.2: Fully; PA 5.1, 5.2: Largely/Fully |

---

## 5. Assessment Indicators (Section 3.3)

Assessment indicators guide an assessor toward objective evidence. There are two types used
in this PAM:

- **Practices** (activity-oriented):
  - **Base Practices (BP)** — apply at capability level 1, indicate extent of achievement of
    process outcomes; always process-specific.
  - **Generic Practices (GP)** — apply at capability levels 1–5, indicate extent of process
    attribute achievement; apply to any process.
- **Information Items (II)** with **Information Item Characteristics (IIC)** — result-oriented
  indicators (Annex B) — "what to look for" when examining an organization's actual work
  products. **No 1:1 mapping** is intended between an information item and the actual work
  product sampled — a single work product may satisfy multiple information item
  characteristics and vice versa.

### 5.1 Information Items vs. Work Products (Section 3.3.2)

- **Information item**: "separately identifiable body of information that is produced,
  stored, and delivered for human use" (ISO/IEC 33001:2015) — used by assessors to judge
  attribute achievement.
- **Work product**: "artifact resulting from the execution of a process" (ISO/IEC/IEEE
  24765:2017) — produced by the assessed organization itself.

> **Relevant framing for Ch.4.4 (Question Bank Design):** this distinction is a good
> academic justification for *why* the tool's questions ask about the presence/quality of
> **evidence** (e.g., "is there a documented software architecture with defined
> interfaces?") rather than prescribing one fixed document template — matching the PAM's own
> stance that "a PRM/PAM does not predefine any particular work product structure" (Section
> 3.3.4).

### 5.2 Why a PRM/PAM Is Not a Lifecycle Model (Section 3.3.4)

A PRM/PAM operates at the **"What"** level of abstraction (goals/outcomes of a process),
deliberately abstracting away from the **"How"** (methods, concrete workflows, tooling) and
the **"Doing"** (actual execution) — see Figure 4 in the source PDF. It "neither predefines,
nor discourages, any order in which... Base Practices are to be performed," and does not
mandate one fixed document per process. This is directly citable when justifying why the
tool's CMAB engine is free to *select* base-practice-aligned questions adaptively rather than
work through a fixed checklist in a fixed order.

---

## 6. The SWE Process Group — Full Definitions (Section 4.4)

This is the **core process group** the thesis's question bank (`AuditQuestion.process`,
`AuditQuestion.base_practice_id`) is built on. Full purpose, outcomes, base practices, and
BP→outcome / info-item→outcome mappings are reproduced below for all six processes.

### 6.1 SWE.1 — Software Requirements Analysis

**Purpose:** Establish a structured and analyzed set of software requirements consistent
with the system requirements and the system architecture.

**Outcomes:**
1. Software requirements are specified.
2. Software requirements are structured and prioritized.
3. Software requirements are analyzed for correctness and technical feasibility.
4. The impact of software requirements on the operating environment is analyzed.
5. Consistency and bidirectional traceability are established between software requirements and system requirements.
6. Consistency and bidirectional traceability are established between software requirements and system architecture.
7. The software requirements are agreed and communicated to all affected parties.

**Base Practices:**
- **BP1 — Specify software requirements.** Use system requirements and system architecture to identify and document functional and non-functional software requirements per defined characteristics (verifiability, unambiguity, freedom from design/implementation, no contradictions).
- **BP2 — Structure software requirements.** Structure and prioritize (e.g., by functionality, product variants, release scope).
- **BP3 — Analyze software requirements.** Analyze correctness, technical feasibility, and interdependencies; support project estimates.
- **BP4 — Analyze the impact on the operating environment.**
- **BP5 — Ensure consistency and establish bidirectional traceability.** Between SW requirements ↔ system architecture, and SW requirements ↔ system requirements.
- **BP6 — Communicate agreed software requirements and impact on the operating environment.**

**Output information items:** Requirement (17-00), Requirement Attribute (17-54), Analysis Results (15-51), Consistency Evidence (13-51), Communication Evidence (13-52).

**BP → Outcome mapping:** BP1→O1, BP2→O2, BP3→O3, BP4→O4, BP5→O5+O6, BP6→O7.

---

### 6.2 SWE.2 — Software Architectural Design

**Purpose:** Establish an analyzed software architecture, comprising static and dynamic
aspects, consistent with the software requirements.

**Outcomes:**
1. A software architecture is designed including static and dynamic aspects.
2. The software architecture is analyzed against defined criteria.
3. Consistency and bidirectional traceability are established between software architecture and software requirements.
4. The software architecture is agreed and communicated to all affected parties.

**Base Practices:**
- **BP1 — Specify static aspects of the software architecture.** External interfaces, defined set of software components with their interfaces and relationships.
- **BP2 — Specify dynamic aspects of the software architecture.** Behavior of components, interaction in different software modes, concurrency aspects.
- **BP3 — Analyze software architecture.** Technical design aspects, project estimates, documented design rationale.
- **BP4 — Ensure consistency and establish bidirectional traceability** (architecture ↔ requirements).
- **BP5 — Communicate agreed software architecture.**

**Output information items:** Software Architecture (04-04), Consistency Evidence (13-51), Communication Evidence (13-52), Analysis Results (15-51).

**BP → Outcome mapping:** BP1+BP2→O1, BP3→O2, BP4→O3, BP5→O4.

---

### 6.3 SWE.3 — Software Detailed Design and Unit Construction

**Purpose:** Establish a software detailed design, comprising static and dynamic aspects,
consistent with the software architecture, and construct software units consistent with the
detailed design.

**Outcomes:**
1. A detailed design is specified including static and dynamic aspects.
2. Software units as specified in the detailed design are produced.
3. Consistency and bidirectional traceability established: detailed design ↔ architecture; source code ↔ detailed design; detailed design ↔ requirements.
4. The source code and agreed detailed design are communicated to all affected parties.

**Base Practices:**
- **BP1 — Specify the static aspects of the detailed design.** Behavior of software units, static structure/relationships, interfaces incl. valid data value ranges and measurement units.
- **BP2 — Specify dynamic aspects of the detailed design.** Interactions between software units.
- **BP3 — Develop software units.** Consistent with detailed design, per coding principles (e.g., no implicit type conversions, single entry/exit point, range checks/defensive programming).
- **BP4 — Ensure consistency and establish bidirectional traceability** (detailed design ↔ architecture; units ↔ detailed design; detailed design ↔ requirements).
- **BP5 — Communicate agreed software detailed design and developed software units.**

**Output information items:** Software Detailed Design (04-05), Software Unit (11-05), Consistency Evidence (13-51), Communication Evidence (13-52).

**BP → Outcome mapping:** BP1+BP2→O1, BP3→O2, BP4→O3, BP5→O4.

---

### 6.4 SWE.4 — Software Unit Verification

**Purpose:** Verify that software units are consistent with the software detailed design.

**Outcomes:**
1. Verification measures for software unit verification are specified.
2. Software unit verification measures are selected according to the release scope, including regression criteria.
3. Software units are verified using the selected measures, and results are recorded.
4. Consistency and bidirectional traceability established between verification measures and software units; bidirectional traceability between verification results and measures.
5. Results are summarized and communicated to all affected parties.

**Base Practices:**
- **BP1 — Specify software unit verification measures.** Pass/fail criteria, entry/exit criteria, required infrastructure. *(Note: examples given are static analysis, code reviews, unit testing; static analysis may use MISRA rulesets.)*
- **BP2 — Select software unit verification measures.** Per selection criteria incl. regression.
- **BP3 — Verify software units.** Record pass/fail and verification measure data.
- **BP4 — Ensure consistency and establish bidirectional traceability.**
- **BP5 — Summarize and communicate results.**

**Output information items:** Verification Measure (08-60), Verification Measure Data (03-50), Verification Measure Selection Set (08-58), Verification Results (15-52), Consistency Evidence (13-51), Communication Evidence (13-52).

**BP → Outcome mapping:** BP1→O1, BP2→O2, BP3→O3, BP4→O4, BP5→O5.

---

### 6.5 SWE.5 — Software Component Verification and Integration Verification

**Purpose:** Verify that software components are consistent with the software architectural
design, and integrate software elements and verify that the integrated software elements are
consistent with the software architecture and detailed design.

**Outcomes:**
1. Verification measures specified for software integration verification of integrated elements based on architecture and detailed design, incl. interfaces/interactions between components.
2. Verification measures specified for software components to provide evidence of compliance with the components' behavior and interfaces.
3. Software elements are integrated up to a complete integrated software.
4. Verification measures selected according to release scope, incl. regression criteria.
5. Software components verified using selected measures; results recorded.
6. Integrated software elements verified using selected measures; results recorded.
7. Consistency and bidirectional traceability established between verification measures and architecture/detailed design; bidirectional traceability between results and measures.
8. Results of software component verification and integration verification summarized and communicated.

**Base Practices:**
- **BP1 — Specify software integration verification measures.** Sequence/preconditions for integrating elements, against static/dynamic architecture aspects.
- **BP2 — Specify verification measures for verifying software component behavior.** Against defined component behavior/interfaces (distinct from unit verification in SWE.4).
- **BP3 — Select verification measures.** Per selection criteria incl. continuous integration/regression.
- **BP4 — Integrate software elements and perform integration verification.** Big-bang, continuous, or stepwise integration with accompanying verification.
- **BP5 — Perform software component verification.**
- **BP6 — Ensure consistency and establish bidirectional traceability.**
- **BP7 — Summarize and communicate results.**

**Output information items:** Verification Measure (08-60), Integration Sequence Instruction (06-50), Verification Measure Data (03-50), Verification Measure Selection Set (08-58), Verification Results (15-52), Consistency Evidence (13-51), Communication Evidence (13-52), Software Component (01-03), Integrated Software (01-50).

**BP → Outcome mapping:** BP1→O1, BP2→O2, BP3→O4, BP4→O3+O6, BP5→O5, BP6→O7, BP7→O8.

---

### 6.6 SWE.6 — Software Verification

**Purpose:** Ensure that the integrated software is verified to be consistent with the
software requirements.

**Outcomes:**
1. Verification measures for software verification specified based on software requirements.
2. Verification measures selected according to release scope, incl. regression criteria.
3. The integrated software is verified using selected measures; results recorded.
4. Consistency and bidirectional traceability established between verification measures and software requirements; bidirectional traceability between results and measures.
5. Results summarized and communicated to all affected parties.

**Base Practices:**
- **BP1 — Specify verification measures for software verification.** Techniques may depend on requirement content (boundary values/equivalence classes, positive vs. negative/fault-injection testing, requirements-based testing vs. error guessing).
- **BP2 — Select verification measures.**
- **BP3 — Verify the integrated software.**
- **BP4 — Ensure consistency and establish bidirectional traceability.**
- **BP5 — Summarize and communicate results.**

**Output information items:** Verification Measure (08-60), Verification Measure Data (03-50), Verification Measure Selection Set (08-58), Verification Results (15-52), Consistency Evidence (13-51), Communication Evidence (13-52).

**BP → Outcome mapping:** BP1→O1, BP2→O2, BP3→O3, BP4→O4, BP5→O5.

---

## 7. Process Capability Levels 1–3 — Full Generic Practices (Section 5.1–5.4)

These are the **only capability levels the tool implements** (`L1 = Performed`, `L2 =
Managed`, `L3 = Established`). Levels 4–5 are summarized in §4.1 above only.

### 7.1 Level 0 — Incomplete process (Section 5.1)

"The process is not implemented or fails to achieve its process purpose. At this level there
is little or no evidence of any systematic achievement of the process purpose." No generic
practices/information items are defined for level 0 (there is no process attribute at this
level).

### 7.2 Level 1 — Performed process — PA 1.1 (Section 5.2.1)

**Scope:** "A measure of the extent to which the process purpose is achieved."

**Achievement:** (1) The process achieves its defined outcomes.

**Generic Practice:**
- **GP 1.1.1 — Achieve the process outcomes.** Achieve the intent of the base practices; produce work products that evidence the process outcomes.

**Output information items:** process-specific information items as described per-process in Section 4 (i.e., the SWE.1–6 output items listed above).

---

### 7.3 Level 2 — Managed process (Section 5.3)

#### PA 2.1 — Process Performance Management (Section 5.3.1)

**Scope:** "A measure of the extent to which the performance of the process is managed."

**Achievements:**
1. Strategy for process performance defined based on identified objectives.
2. Performance of the process is planned.
3. Performance is monitored and adjusted to meet the planning.
4. Needs for human resources (incl. responsibilities/authorities) determined.
5. Needs for physical/material resources determined.
6. Persons performing the process are prepared for their responsibilities.
7. Physical/material resources are identified, made available, allocated, used.
8. Interfaces between involved parties are managed for communication and responsibility assignment.

**Generic Practices:**
- **GP 2.1.1 — Identify the objectives and define a strategy for the performance of the process.** Scope, corresponding results, performance objectives/criteria, assumptions/constraints, approach/methodology.
- **GP 2.1.2 — Plan the performance of the process.** Activities and work packages, estimates (schedule, milestones).
- **GP 2.1.3 — Determine resource needs.** Human resources/skills, physical/material resources, responsibilities/authorities.
- **GP 2.1.4 — Identify and make available resources.** Allocate individuals, qualify them (training/mentoring/coaching), make other resources available.
- **GP 2.1.5 — Monitor and adjust the performance of the process.** Identify deviations, take action, adjust planning.
- **GP 2.1.6 — Manage the interfaces between involved parties.** Determine individuals/groups, assign responsibilities, determine and maintain communication mechanisms.

**Output information items:** Process performance strategy (19-01), Process performance objectives (18-58), Work package (14-10), Schedule (08-56), Progress status (13-14), Resource needs (17-55), Resource allocation (08-61), Communication matrix (08-62), Communication evidence (13-52).

#### PA 2.2 — Work Product Management (Section 5.3.2)

**Scope:** "A measure of the extent to which the work products produced by the process are appropriately managed."

**Achievements:**
1. Requirements for work products of the process are defined.
2. Requirements for storage and control of work products are defined.
3. Work products are appropriately identified, stored, and controlled.
4. Work products are reviewed and adjusted as necessary to meet requirements.

**Generic Practices:**
- **GP 2.2.1 — Define the requirements for the work products.** Content/structure, quality criteria, review/approval criteria.
- **GP 2.2.2 — Define the requirements for storage and control of the work products.** Identification, distribution; status models (e.g., "Under Work", "Tested", "Released").
- **GP 2.2.3 — Identify, store and control the work products.** Change control; versioning/baselining; availability with revision status.
- **GP 2.2.4 — Review and adjust work products.** Against defined requirements/criteria; ensure issue resolution.

**Output information items:** Requirements for work products (17-05), Review and approval criteria (18-59), Quality criteria (18-07), Review evidence (13-19), Baseline (13-08), Repository (16-00).

> **Relevant for Ch.4.6 (Weakness Classifier) / Ch.2:** PA 2.1 and PA 2.2 map naturally onto
> "process management" (planning, monitoring, resourcing) vs. "artifact management"
> (documentation quality, review, version control) — a useful two-axis framing if the
> thesis wants to argue *why* L2 questions in the seeded bank tend to split between
> "is there a plan/schedule/tracking?" and "is the work product reviewed/baselined/stored
> properly?".

---

### 7.4 Level 3 — Established process (Section 5.4)

#### PA 3.1 — Process Definition (Section 5.4.1)

**Scope:** "A measure of the extent to which a standard process is maintained to support the deployment of the defined process."

**Achievements:**
1. A standard process is developed, established, and maintained describing the fundamental elements incorporated into a defined process.
2. Required inputs and expected outputs for the standard process are defined.
3. Roles, responsibilities, authorities, and required competencies are defined.
4. Tailoring guidelines for deriving the defined process from the standard process are defined.
5. Required physical/material resources and process infrastructure needs are determined.
6. Suitable methods and required activities for monitoring effectiveness/suitability/adequacy are determined.

**Generic Practices:**
- **GP 3.1.1 — Establish and maintain the standard process.** Activities/interactions, inputs/outputs with entry/exit criteria, process performance roles (e.g., RASIC), guidance/procedures/templates, tailoring guidelines, maintenance per feedback.
- **GP 3.1.2 — Determine the required competencies.** Skills/knowledge/experience per role; qualification methods (training, mentoring, self-study).
- **GP 3.1.3 — Determine the required resources.** Physical/material resources, process infrastructure.
- **GP 3.1.4 — Determine suitable methods to monitor the standard process.** Lessons learned, compliance checks, internal audits, management reviews, change requests, state-of-the-art comparison.

**Output information items:** Tailoring guideline (06-51), Process monitoring method (08-63), Process description (10-00), Role description (10-50), Qualification method description (10-51), Process resource and infrastructure description (10-52).

#### PA 3.2 — Process Deployment (Section 5.4.2)

**Scope:** "A measure of the extent to which the standard process is deployed as a defined process to achieve its process outcomes."

**Achievements:**
1. A defined process is deployed based upon an appropriately selected/tailored standard process.
2. Assignment of persons to roles is performed and communicated.
3. Required education/training/experience is ensured and monitored.
4. Required resources are made available, allocated, and maintained.
5. Appropriate information is collected and analyzed to understand the behavior of the process.

**Generic Practices:**
- **GP 3.2.1 — Deploy a defined process that satisfies the context specific requirements of the use of the standard process.** Select/tailor, verify conformance, use as managed process.
- **GP 3.2.2 — Ensure required competencies for the defined roles.** Allocate per competencies, communicate assignments, identify/close skill gaps, monitor staff availability.
- **GP 3.2.3 — Ensure required resources to support the performance of the defined process.** Information, physical/material resources, infrastructure; measure/monitor usage.
- **GP 3.2.4 — Monitor the performance of the defined process.** Collect/analyze per determined monitoring methods; feed results back for continual improvement (cross-ref: PIM.3).

**Output information items:** Process description (10-00), Tailoring documentation (15-54), Role assignment (14-53), Process resource and infrastructure documentation (13-55), Process performance information (03-06).

> **Relevant for Ch.2/Ch.8 (Future Work):** PA 3.x is squarely about *organizational*
> maturity (a maintained standard process, tailoring guidelines, competency management) —
> which is explicitly **out of scope** for a self-service, session-based web tool answered
> by individual stakeholders rather than assessed via organizational audit evidence. This is
> a legitimate, citable **limitation** to name explicitly in Ch.7.6/Ch.8.3: the tool
> approximates L3 questions from an individual stakeholder's perspective ("do you know of a
> tailoring guideline / role description / standard template?") rather than performing a
> genuine organizational-level PA 3.1/3.2 assessment, which by definition requires
> examining organizational assets, not one respondent's session answers.

---

## 8. Selected Information Item Characteristics (subset of Annex B, p.122–142)

Only entries directly referenced by the SWE.1–6 process descriptions above are kept.

| ID | Name | Key characteristics |
|---|---|---|
| 01-03 | Software component | Software element above unit level; design model element or executable code + config description. |
| 01-50 | Integrated software | Software executable incl. application parameter files and all configured elements. |
| 03-50 | Verification Measure data | Data recorded during execution of a verification measure (test raw data/logs/traces, measurement values, calculation values, simulation protocol, review findings, analysis values). |
| 04-04 | Software architecture | Justifying rationale; individual functional/non-functional behavior of components; interface technical characteristics (sync of processes/tasks, programming-language calls, APIs, method definitions, callback functions); dynamics (logical operating modes, intercommunication/priority, time slices, interrupts, interactions); explanatory annotations. |
| 04-05 | Software detailed design | Control flow definition, input/output data format, algorithms, defined data structures, justified global variables, explanatory annotations. Expression languages range from natural language to semi-formal (UML/SysML) to formal (model-based), depending on complexity/criticality. |
| 08-58 | Verification Measure Selection Set | Includes criteria for re-verification (regression); identification of verification measures incl. regression testing. |
| 08-60 | Verification Measure | Can be a test case, measurement, calculation, simulation, review, optical inspection, or analysis. Specification includes pass/fail criteria, entry/exit/abort/re-start criteria, techniques (black-box/white-box, equivalence classes/boundary values, fault injection, penetration testing, back-to-back testing, ICT), verification environment/infrastructure, sequence/ordering. |
| 11-05 | Software Unit | Either a representation of the lowest-level software element in a conceptual model (part of a component), or a representation of a unit under verification (commented source code, auto-code, object file, library, executable, or executable model). |
| 13-51 | Consistency Evidence | Demonstrates bidirectional traceability throughout the life cycle (tool links, hyperlinks, editorial references, naming conventions) *and* evidence that referenced/mapped information coheres semantically (pair working, peer spot checks, revision histories, change commenting). |
| 13-52 | Communication Evidence | Any form of interpersonal communication: e-mails (incl. automated), tool-supported workflows, meetings/minutes (e.g., daily standups), podcasts, blogs, videos, forums, live chat, wikis, photo protocols. |
| 15-51 | Analysis Results | Identification of the object under analysis, analysis criteria used (selection/decision/quality criteria), analysis results (what was decided/selected, reason, assumptions, potential negative impact). Aspects may include correctness, understandability, verifiability, feasibility, validity. |
| 15-52 | Verification Results | Verification data/logs; measure passed/not passed/not executed with rationale; execution info (date, object under verification); abstraction/summary of results. |
| 17-00 | Requirement | An expectation of functions/capabilities or an interface, from a black-box perspective, that is verifiable, unambiguous, free of design/implementation decisions, and non-contradictory. A requirement that implies a design/implementation decision is called a "Design Constraint." |
| 17-54 | Requirement Attribute | Meta-attributes supporting structuring and release-scope definition of requirements (tool-realizable); further supports requirement analysis. |

---

## 9. Key Diagrams and Concepts (Annex C, selected)

### 9.1 "Element", "Component", and "Unit" (Annex C.2, Figure C.2)

Shows how the terms nest across the SYS/SWE V-model:

```
                              Element
  ┌───────────────────────────────────────────────────────────┐
  │ SYS.2 Sys Req Analysis                 SYS.5 Sys Verif.    │
  │   SYS.3 Sys Arch. Design         SYS.4 Sys Integration &   │
  │     SWE.1 SW Req Analysis            Integration Verif.    │
  │                                     SWE.6 SW Verification  │
  │  [Software    SWE.2 SW Arch.    SWE.5 SW Component Verif.  │
  │  Component]      Design           & Integration Verif.     │
  │  [Software    SWE.3 SW Detailed   SWE.4 SW Unit Verif.     │
  │  Unit]        Design & Unit Constr.                        │
  └───────────────────────────────────────────────────────────┘
```

This is the standard's own visual justification for why **SWE.3/SWE.4 operate at the
software-unit level**, **SWE.2/SWE.5 at the software-component level**, and **SWE.1/SWE.6 at
the whole-software level** — directly useful for a figure in Ch.2 (Background) explaining
the granularity progression that the question bank's `base_practice_id` field encodes.

### 9.2 "Agree" vs. "Summarize and Communicate" (Annex C.6, Figure C.5)

The **left side of the V** (requirements/design processes: SYS.2, SYS.3, SWE.1, SWE.2,
SWE.3) uses base practices phrased **"Communicate agreed 'work product x'"** — meaning a
*joint understanding* between affected parties of what the work product means.

The **right side of the V** (verification processes: SWE.4, SWE.5, SWE.6, SYS.4, SYS.5) uses
base practices phrased **"Summarize and communicate results"** — meaning *abstracted*
information from test/verification execution made available to affected parties.

At capability level 1, neither of these communication-oriented practices requires a
planning-based approach or formal approval/release (that is reserved for GP 2.1.6 at level
2) — they simply require the work product/results to be disseminated.

> **Relevant for Ch.4.4.1 (Question Bank Design) or Ch.2:** this left/right-of-the-V
> distinction is a clean way to explain, in the thesis, why the seeded question bank's
> `recommendation_logic` text differs in tone between requirement/design questions
> ("has this been agreed and communicated?") and verification questions ("have results been
> summarized and communicated?") if that pattern was followed during question authoring —
> worth checking against the actual 42-question seed data.

### 9.3 Terminology note — "Verification" instead of "Testing" (Annex C.7)

Automotive SPICE 4.0 deliberately uses the umbrella term **"verification"** rather than
"testing" for SWE.4/5/6 and SYS.4/5, because testing is not the only verification approach —
measurements, calculations/analyses (e.g., FEM stress calculation), and simulations are
equally valid verification measures, especially at the system/hardware level. SWE.4 (Unit
Verification) already exemplified this by combining static analysis, testing, and code
review as equally valid verification techniques (cf. ISO 26262-6 clause 9).

> Useful one-line justification if the thesis's question bank ever asks about
> "verification approach" rather than narrowly about "testing."

---

## 10. What Was Deliberately Left Out

For completeness/traceability, here is what was excluded from this curated file and why:

- **ACQ, SPL, SYS (detailed BPs), VAL, MLE, HWE process groups** — not part of the SWE.1–6
  scope this thesis's question bank covers. SYS is referenced only conceptually above
  (as the upstream input to SWE.1/SWE.2 traceability) — go to the original PDF §4.3 if a
  specific SYS base practice needs to be cited for a traceability example.
- **SUP (except general mention), MAN, PIM, REU** — organizational/supporting processes,
  out of scope for a single-session stakeholder self-assessment tool.
- **Process capability levels 4–5 (PA 4.1, 4.2, 5.1, 5.2)** — out of scope; the tool only
  models L1–L3. Summarized in one table (§4.1) for completeness/future-work framing only.
- **Annex A (Conformity statements)** — legal/standards-compliance boilerplate mapping the
  PAM to ISO/IEC 33004:2015; not relevant to thesis content.
- **Annex B (Information Item Characteristics) in full** — only the ~14 entries actually
  referenced by SWE.1–6 were kept (§8 above); the other ~80 entries (hardware, ML, project
  management, reuse, etc.) were dropped.
- **Annex C.1, C.3, C.4, C.5** — the "Plug-in" concept, MLE integration, example ML
  architecture, and the full traceability diagrams for SYS/HW/ML — not needed since the
  thesis only covers the SWE plug-in scope, and the SWE-specific traceability logic is
  already captured in Annex C.2/C.6 above.
- **Annex D (Reference standards)** — a bare list of ISO/IEC standard numbers; cite directly
  from the PDF only if the bibliography needs a specific ISO/IEC reference entry.
