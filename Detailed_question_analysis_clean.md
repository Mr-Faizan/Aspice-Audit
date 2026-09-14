ASPICE SWE.1–SWE.6 Questionnaire

Weights: 
0 = Best / lowest risk · 
5 = Worst / highest risk (highest CMAB reward).

Stakeholders: 
SD = Software Developer · 
SA = Software Architect · 
PM = Project Manager

QA = QA Engineer · 
TE = Test Engineer · 
TL = Team Lead · 
ASR = ASPICE Assessor.

Levels: 
L1 = Performed · 
L2 = Managed · 
L3 = Established

SWE.1 — Software Requirements Analysis

SWE1_L1_01

ID: SWE1_L1_01

Level: L1

Criteria: SWE.1.BP1 — Specify SW requirements (verifiability, unambiguity)

Identifies: Weak requirement quality, ambiguity, untestable SW requirements

Stakeholder: SA, SD, QA

Question: How are software requirements specified for the current release?

Options:

A) Each requirement is uniquely identified, atomic, verifiable and references its source

B) Requirements are uniquely identified but verifiability criteria are missing for some

C) Requirements exist as free-text paragraphs without unique IDs

D) Requirements are partially captured in slides/e-mails

E) No formal SW requirements set exists

Weights: 0, 2, 3, 4, 5

Recommendation Logic: High weight ⇒ recommend a requirement-specification template aligned with IEEE 29148 + tooling audit (DOORS/Polarion/Jama).

SWE1_L1_02

ID: SWE1_L1_02

Level: L1

Criteria: SWE.1.BP2 — Structure SW requirements

Identifies: Missing prioritisation / categorisation, scope-creep risk

Stakeholder: PM, SA

Question: How are SW requirements categorised and prioritised?

Options:

A) Categorised (functional/non-functional/safety/security) and prioritised against release plan

B) Categorised only

C) Prioritised only

D) Done ad-hoc per request

E) Not categorised or prioritised

Weights: 0, 2, 2, 4, 5

Recommendation Logic: Recommend introducing a categorisation scheme + MoSCoW/RICE prioritisation linked to MAN.3 (out of scope but referenced).

SWE1_L1_03

ID: SWE1_L1_03

Level: L1

Criteria: SWE.1.BP3 — Analyse SW requirements (correctness, technical feasibility)

Identifies: Latent feasibility risk, late re-work

Stakeholder: SA, SD

Question: How is the technical feasibility of new SW requirements analysed before they are baselined?

Options:

A) Formal feasibility review with architect & developer sign-off

B) Informal feasibility check by architect only

C) Feasibility judged during implementation

D) Feasibility never explicitly checked

E) Unknown / no defined approach

Weights: 0, 2, 4, 5, 5

Recommendation Logic: Recommend a feasibility-review checklist gated on requirement baselining.

SWE1_L1_04

ID: SWE1_L1_04

Level: L1

Criteria: SWE.1.BP4 — Analyse impact on operating environment

Identifies: Missed timing / ODD / resource impact

Stakeholder: SA, SD

Question: When SW requirements affect timing, memory, or operating-environment behaviour, how is the impact captured?

Options:

A) Documented impact analysis linked to each affected requirement

B) Captured in design notes only

C) Discussed verbally in reviews

D) Not analysed unless a defect is found

E) No process

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend introducing impact-analysis fields in the requirement template; cross-link to non-functional verification in SWE.6.

SWE1_L1_05

ID: SWE1_L1_05

Level: L1

Criteria: SWE.1.BP5 — Ensure consistency & bidirectional traceability (SYS-req ↔ SW-req ↔ SYS-arch)

Identifies: Broken bidirectional traceability — top assessor finding

Stakeholder: SA, QA, ASR

Question: What is the current state of bidirectional traceability between system requirements and software requirements?

Options:

A) Tool-enforced bidirectional links, audited every release

B) Bidirectional links exist but coverage is partial

C) Only forward links (SYS→SW) exist

D) Traceability is maintained in spreadsheets

E) No traceability data

Weights: 0, 2, 3, 4, 5

Recommendation Logic: High signal: recommend RTM/OSLC tooling audit and a SUP.10 change-impact review procedure (referenced, not in scope).

SWE1_L1_06

ID: SWE1_L1_06

Level: L1

Criteria: SWE.1.BP6 — Communicate agreed SW requirements & impact

Identifies: Lack of agreement → late churn

Stakeholder: PM, SA, TL

Question: How is agreement on the SW requirements baseline reached and recorded?

Options:

A) Formal review meeting with signed-off minutes per release

B) Review meeting without recorded sign-off

C) E-mail confirmation only

D) Implicit agreement, no record

E) No agreement step

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend introducing a lightweight "Requirements Agreement Record" gate.

SWE1_L2_07

ID: SWE1_L2_07

Level: L2

Criteria: GP 2.1.1, GP 2.1.2 — Performance objectives & planning for SWE.1

Identifies: Missing/weak strategy for the requirements process

Stakeholder: PM, QA

Question: How is the SWE.1 process planned and monitored at project level?

Options:

A) Documented requirements-engineering plan with KPIs (e.g., review backlog, churn) reviewed monthly

B) Plan exists but KPIs are not tracked

C) Activities scheduled in MS-Project only

D) Planned ad-hoc per sprint

E) No plan

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Indicates PA 2.1 weakness; recommend a requirements KPI dashboard.

SWE.2 — Software Architectural Design

SWE2_L1_01

ID: SWE2_L1_01

Level: L1

Criteria: SWE.2.BP1 — Specify static aspects of architecture

Identifies: Missing decomposition / structural views

Stakeholder: SA

Question: How is the static structure of the SW architecture documented?

Options:

A) Hierarchical component model with explicit interfaces, in a modelling tool (UML/SysML/EA)

B) Block diagrams in modelling tool, no interface model

C) PowerPoint diagrams

D) Textual description only

E) Not documented

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend a model-based architecture in EA/Cameo; flag tool break to traceability.

SWE2_L1_02

ID: SWE2_L1_02

Level: L1

Criteria: SWE.2.BP2 — Specify dynamic aspects (timing, sequences, state)

Identifies: Hidden timing/concurrency defects

Stakeholder: SA, SD

Question: How are dynamic aspects (timing, sequencing, state) specified for the architecture?

Options:

A) Sequence + state diagrams + timing budgets per component

B) Sequence diagrams only

C) Narrative timing notes

D) Implicit, decided during coding

E) Not specified

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend timing-budget table; pair with SWE.5 integration tests.

SWE2_L1_03

ID: SWE2_L1_03

Level: L1

Criteria: SWE.2.BP3 — Analyse architecture, justify chosen design (PAM 4.0 replaces former "evaluate alternatives" BP)

Identifies: Unjustified architecture, hidden trade-offs

Stakeholder: SA, ASR

Question: How is the chosen architecture justified against alternatives and quality criteria (modularity, reliability, security)?

Options:

A) Documented trade-off analysis with rationale recorded per decision

B) Decision log with brief rationale

C) Verbal discussion in design review

D) Not justified, "as-is"

E) Decision-maker unknown

Weights: 0, 2, 3, 4, 5

Recommendation Logic: High signal: recommend architecture-decision-record (ADR) practice.

SWE2_L1_04

ID: SWE2_L1_04

Level: L1

Criteria: SWE.2.BP3 — interfaces & resource consumption

Identifies: Interface ambiguity, resource overruns at HIL/qualification

Stakeholder: SA, SD

Question: How are interfaces and resource-consumption objectives (RAM/ROM/CPU/bandwidth) defined for SW components?

Options:

A) Each interface fully typed; RAM/ROM/CPU budgets per component

B) Interfaces typed; no resource budgets

C) Resource budgets only at SW level (not per component)

D) Defined only when problems arise

E) Not defined

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend interface contracts + per-component budgets; verify with static analysis (SWE.4).

SWE2_L1_05

ID: SWE2_L1_05

Level: L1

Criteria: SWE.2.BP4 — Consistency & bidirectional traceability (SW-req ↔ SW-arch)

Identifies: Architecture/requirement drift

Stakeholder: SA, QA, ASR

Question: How is bidirectional traceability maintained between SW requirements and architectural elements?

Options:

A) Tool-enforced (allocation column / OSLC link) and reviewed each baseline

B) Maintained but not periodically audited

C) Manual matrix in spreadsheet

D) Allocation is implicit

E) No traceability

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend OSLC-style linking; tie to SWE.1 traceability question to detect compounded weakness.

SWE2_L1_06

ID: SWE2_L1_06

Level: L1

Criteria: SWE.2.BP5 — Communicate agreed architecture

Identifies: Architecture not internalised by team

Stakeholder: SA, TL

Question: How is the agreed architecture communicated and made available to development and test teams?

Options:

A) Published in the team wiki + walk-through workshop with attendance log

B) Published in wiki only

C) Sent by e-mail

D) Available on request

E) Not communicated

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend onboarding workshop + searchable architecture site.

SWE2_L2_07

ID: SWE2_L2_07

Level: L2

Criteria: GP 2.2.1, GP 2.2.4 — Work-product requirements & review for architecture artefacts

Identifies: Architecture artefacts not reviewed against criteria

Stakeholder: QA, ASR

Question: How are architecture work products (model, ADRs, interface specs) reviewed and approved?

Options:

A) Defined review checklist + approver role + review record per baseline

B) Review checklist but no approver role

C) Reviews held without checklist

D) Reviews held only when issues escalate

E) No reviews

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Indicates PA 2.2 weakness; recommend SUP.1-style work-product review template.

SWE.3 — Software Detailed Design and Unit Construction

SWE3_L1_01

ID: SWE3_L1_01

Level: L1

Criteria: SWE.3.BP1 — Specify static aspects of detailed design

Identifies: Skipping detailed design, "code-is-design" antipattern

Stakeholder: SA, SD

Question: How is the static detailed design of software units captured?

Options:

A) Class/data structure model in tool, generated from architecture

B) Diagrams in modelling tool, manually maintained

C) Text-and-code-comments only

D) Comments in source code

E) No detailed design

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend keeping design synchronised via code-from-model or model-from-code.

SWE3_L1_02

ID: SWE3_L1_02

Level: L1

Criteria: SWE.3.BP2 — Specify dynamic aspects of detailed design

Identifies: Hidden control-flow / state defects

Stakeholder: SD, SA

Question: How are state machines, control flows, and unit interactions described?

Options:

A) State/sequence diagrams per non-trivial unit

B) Diagrams only for safety-critical units

C) Narrative description

D) Discovered during coding

E) Not described

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend state-chart coverage for safety-critical paths.

SWE3_L1_03

ID: SWE3_L1_03

Level: L1

Criteria: SWE.3.BP3 — Develop software units (coding standard adherence)

Identifies: Coding-standard violations, MISRA gaps

Stakeholder: SD, QA

Question: How are coding standards (e.g., MISRA C/C++, AUTOSAR C++14) enforced during unit construction?

Options:

A) Pre-commit check + CI gate blocks merges on standard violations

B) CI gate runs but does not block merges

C) Periodic audit by QA

D) Standard exists but is not enforced

E) No coding standard adopted

Weights: 0, 2, 3, 4, 5

Recommendation Logic: High signal: recommend Axivion/Polyspace/Coverity gate; flag SWE.4 static-analysis question for re-check.

SWE3_L1_04

ID: SWE3_L1_04

Level: L1

Criteria: SWE.3.BP4 — Consistency & bidirectional traceability (SW-req ↔ arch ↔ detailed design ↔ units)

Identifies: Multi-hop traceability gap

Stakeholder: SA, QA, ASR

Question: What is the state of traceability from architecture → detailed design → source units?

Options:

A) End-to-end tool-enforced, audited each release

B) Forward links complete; reverse links partial

C) Spreadsheet only

D) Traceability stops at design level

E) No links

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Strongest predictor of CL2 failure across SWE.3; recommend OSLC link consolidation.

SWE3_L1_05

ID: SWE3_L1_05

Level: L1

Criteria: SWE.3.BP5 — Communicate agreed detailed design and units

Identifies: Knowledge silo, single-point-of-failure

Stakeholder: SD, TL

Question: How are agreed detailed design and developed units made available to peers and testers?

Options:

A) Reviewed pull requests + design documented in shared repo

B) Code committed, design in shared repo

C) Code only, design private to developer

D) Code on local branches, no design

E) Knowledge held by one developer

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend mandatory peer review and shared design index.

SWE3_L2_06

ID: SWE3_L2_06

Level: L2

Criteria: GP 2.1.5 — Monitor & adjust process (defect/rework rates per unit)

Identifies: No control loop for code quality

Stakeholder: TL, QA, PM

Question: How is the SWE.3 process monitored at project level (e.g., rework, defect density per unit)?

Options:

A) Defect-density and rework metrics tracked weekly with thresholds

B) Metrics tracked monthly, no thresholds

C) Metrics gathered only for assessments

D) No monitoring beyond burndown

E) Not monitored

Weights: 0, 2, 3, 4, 5

Recommendation Logic: PA 2.1 weakness; recommend defect-density dashboard and threshold-based escalation.

SWE3_L3_07

ID: SWE3_L3_07

Level: L3

Criteria: GP 3.1.1, GP 3.1.4 — Standard process & tailoring guidelines

Identifies: Project-specific drift from organisational standard

Stakeholder: ASR, QA, PM

Question: How is the organisation’s standard SWE.3 process tailored for this project?

Options:

A) Tailoring documented against tailoring guidelines, reviewed by Process Group

B) Tailoring documented, not reviewed

C) Project follows standard process verbatim, no tailoring

D) Tailoring done informally

E) No standard process exists

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Note: option C is mid-risk because lack of tailoring often hides cargo-cult adoption; recommend formal tailoring record.

SWE.4 — Software Unit Verification

SWE4_L1_01

ID: SWE4_L1_01

Level: L1

Criteria: SWE.4.BP1 — Specify unit-verification measures (tactic)

Identifies: Missing verification tactic

Stakeholder: TE, SD

Question: How are unit-verification measures (test cases, static analysis, coverage goals) specified?

Options:

A) Documented per component, derived from detailed design and non-functional reqs

B) Documented but not derived from non-functional reqs

C) Test cases only, no static-analysis measures

D) Specified ad-hoc

E) Not specified

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend a unit-verification specification template with derivation columns.

SWE4_L1_02

ID: SWE4_L1_02

Level: L1

Criteria: SWE.4.BP2 — Select verification measures incl. regression

Identifies: Insufficient regression coverage

Stakeholder: TE

Question: How are verification measures selected per release, including regression?

Options:

A) Selection rules documented and applied per release; regression set auto-derived from change-impact

B) Regression decided manually each release

C) Always run all unit tests

D) Regression decided only when defects appear

E) No selection mechanism

Weights: 0, 2, 2, 4, 5

Recommendation Logic: High signal for late-stage defects; recommend change-impact-driven regression.

SWE4_L1_03

ID: SWE4_L1_03

Level: L1

Criteria: SWE.4.BP3 — Verify (static + dynamic)

Identifies: Weak static analysis

Stakeholder: SD, QA

Question: How is static analysis performed on software units?

Options:

A) Tool integrated in CI; zero high-severity findings policy

B) Tool integrated in CI; findings tracked but not blocking

C) Manual code reviews only

D) Static analysis runs only before milestones

E) Not performed

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Reinforces SWE3_L1_03; recommend severity-based blocking gate.

SWE4_L1_04

ID: SWE4_L1_04

Level: L1

Criteria: SWE.4.BP3 — Test SW units & record results (coverage)

Identifies: Inadequate structural coverage

Stakeholder: TE, SD

Question: What unit-test coverage criteria are applied for non-safety code?

Options:

A) Statement + branch coverage with documented threshold (e.g., ≥ 90 % branch)

B) Statement coverage threshold only

C) Coverage measured but no threshold

D) Coverage measured ad-hoc

E) Not measured

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend MC/DC for ASIL B+ paths; align thresholds with ISO 26262 (referenced).

SWE4_L1_05

ID: SWE4_L1_05

Level: L1

Criteria: SWE.4.BP4 — Bidirectional traceability between units, criteria, results

Identifies: Test-result orphaning

Stakeholder: TE, QA, ASR

Question: How are unit-test results linked to verification criteria and units?

Options:

A) Tool-enforced bidirectional links; audited each release

B) Manual matrix maintained

C) Links exist for failed tests only

D) Linked only when assessor asks

E) Not linked

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend test-management tool integration (e.g., qTest/Jama/Polarion).

SWE4_L2_06

ID: SWE4_L2_06

Level: L2

Criteria: GP 2.1.6, GP 2.1.7 — Resources & stakeholder management for SWE.4

Identifies: Under-resourced verification, late access to HW/test bench

Stakeholder: PM, TL, TE

Question: How is access to test infrastructure (HIL/SIL, test benches, target boards) planned and assured for unit verification?

Options:

A) Infrastructure capacity planned per release; bottleneck escalation defined

B) Plan exists but no escalation path

C) Access requested per sprint

D) Access negotiated when needed

E) Frequent blocking due to unavailable HW

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Strongest "release-phase" predictor; recommend resource calendar + escalation.

SWE4_L2_07

ID: SWE4_L2_07

Level: L2

Criteria: GP 2.2.3, GP 2.2.4 — Work-product control & review of unit-verification reports

Identifies: Reports not under configuration control

Stakeholder: QA

Question: How are unit-verification reports stored, versioned, and reviewed?

Options:

A) Versioned in CM with status workflow + reviewer sign-off

B) Versioned only

C) Stored on shared drive, no versioning

D) Stored locally

E) Not formally stored

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend CM-controlled report storage (referenced SUP.8).

SWE.5 — Software Component Verification and Integration Verification

SWE5_L1_01

ID: SWE5_L1_01

Level: L1

Criteria: SWE.5.BP1 — Specify integration-verification measures

Identifies: Missing integration-verification scope

Stakeholder: TE, SA

Question: How are integration-verification measures defined for the integrated software?

Options:

A) Per-component and per-interface measures derived from architecture

B) Per-component only

C) End-to-end tests only

D) Defined as needed

E) Not defined

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend interface-driven integration-verification specs.

SWE5_L1_02

ID: SWE5_L1_02

Level: L1

Criteria: SWE.5.BP2 — Specify component-behaviour verification measures (PAM 4.0 novelty)

Identifies: Component-level black-box gaps

Stakeholder: TE, SA

Question: How is software-component behaviour verified before integration?

Options:

A) Component contract tests run against published interfaces in CI

B) Component tests exist but run manually

C) Verified only as part of integration

D) Verified only at qualification

E) Not verified at component level

Weights: 0, 2, 3, 4, 5

Recommendation Logic: New PAM 4.0 expectation; high signal of legacy 3.1 process.

SWE5_L1_03

ID: SWE5_L1_03

Level: L1

Criteria: SWE.5.BP3 — Select verification measures incl. regression

Identifies: Selection criteria absent

Stakeholder: TE

Question: How are integration-test cases selected per release (including regression)?

Options:

A) Selection rules + change-impact-driven regression set documented

B) Regression rules only

C) "Run everything"

D) Selected ad-hoc

E) No selection criteria

Weights: 0, 2, 2, 4, 5

Recommendation Logic: Recommend traceable selection rules linked to release scope.

SWE5_L1_04

ID: SWE5_L1_04

Level: L1

Criteria: SWE.5.BP4 — Integrate elements & perform integration verification

Identifies: Big-bang integration risk

Stakeholder: SD, TE, SA

Question: How are software elements integrated and verified?

Options:

A) Continuous integration with stepwise integration plan and per-step verification

B) Stepwise integration but verification batched

C) Daily integration without integration plan

D) Big-bang integration at end of sprint

E) Big-bang integration at end of release

Weights: 0, 2, 3, 4, 5

Recommendation Logic: High signal of late defects; recommend stepwise integration plan with CI.

SWE5_L1_05

ID: SWE5_L1_05

Level: L1

Criteria: SWE.5.BP5 — Perform component verification & record

Identifies: Result records missing

Stakeholder: QA, TE

Question: How are component-verification and integration-verification results recorded?

Options:

A) Recorded automatically in test-management tool with status, evidence, environment metadata

B) Recorded in test tool, no environment metadata

C) Captured in spreadsheets

D) Captured in e-mail/chat

E) Not recorded

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend tool-based recording with environment fingerprint.

SWE5_L1_06

ID: SWE5_L1_06

Level: L1

Criteria: SWE.5.BP6 — Consistency & bidirectional traceability (arch / detailed design ↔ verification measures ↔ results)

Identifies: Verification-result orphaning at integration

Stakeholder: QA, ASR

Question: What is the state of bidirectional traceability between architecture/design, integration verification measures, and results?

Options:

A) Tool-enforced bidirectional links with periodic audits

B) Forward only

C) Spreadsheet matrix

D) Implicit

E) None

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Compose with SWE2_L1_05 for compounded signal.

SWE5_L2_07

ID: SWE5_L2_07

Level: L2

Criteria: GP 2.1.4 — Adjust process performance (interface management between SD & integration team)

Identifies: Interface miscommunication between teams

Stakeholder: TL, PM

Question: How are interface changes coordinated between development and integration teams?

Options:

A) Interface change board with affected-party notification SLA

B) E-mail notification policy in place

C) Notified during integration only

D) Discovered during failure

E) No coordination mechanism

Weights: 0, 2, 3, 4, 5

Recommendation Logic: PA 2.1 / GP 2.1.7 (involved-party management); recommend lightweight ICB.

SWE.6 — Software Verification (formerly Software Qualification Test)

SWE6_L1_01

ID: SWE6_L1_01

Level: L1

Criteria: SWE.6.BP1 — Specify verification measures vs. SW requirements

Identifies: Test cases not derived from SW requirements

Stakeholder: TE

Question: How are software-verification measures derived from SW requirements?

Options:

A) Each SW requirement has at least one verification measure recorded with technique justification

B) Coverage exists but technique not justified

C) Coverage is partial

D) Tests written from intuition

E) Not derived from SW requirements

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend req-to-test allocation report at each baseline.

SWE6_L1_02

ID: SWE6_L1_02

Level: L1

Criteria: SWE.6.BP2 — Select verification measures incl. regression (release scope)

Identifies: Regression policy weak at qualification

Stakeholder: TE, PM

Question: How are SWE.6 verification measures selected for the release, including regression?

Options:

A) Documented selection per release with risk-based regression set

B) Selection per release without risk weighting

C) Always full re-run

D) Selected verbally per stand-up

E) No selection process

Weights: 0, 2, 2, 4, 5

Recommendation Logic: High signal pre-release; flag if release phase = late.

SWE6_L1_03

ID: SWE6_L1_03

Level: L1

Criteria: SWE.6.BP3 — Verify integrated SW & record (qualification environment)

Identifies: Wrong target / non-representative env.

Stakeholder: TE, QA

Question: What environment is used for SWE.6 qualification verification?

Options:

A) Representative target HW (HIL/real ECU) with calibrated parameters

B) HIL only

C) SIL/MIL with HW abstraction

D) PC simulation

E) Developer machine

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend escalation to HIL for safety-critical functions.

SWE6_L1_04

ID: SWE6_L1_04

Level: L1

Criteria: SWE.6.BP4 — Consistency & bidirectional traceability (SW reqs ↔ test specs ↔ results)

Identifies: Final-stage traceability gap

Stakeholder: QA, ASR

Question: How is bidirectional traceability maintained between SW requirements, qualification test specs, and results?

Options:

A) Tool-enforced and audited each release

B) Maintained but not audited

C) Spreadsheet

D) Manual when needed

E) None

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Compose with SWE1_L1_05; if both high → critical traceability red flag.

SWE6_L1_05

ID: SWE6_L1_05

Level: L1

Criteria: SWE.6.BP5 — Summarise & communicate results

Identifies: Defect leakage / no test summary

Stakeholder: QA, PM

Question: How are qualification-test results summarised and communicated to affected parties?

Options:

A) Versioned test-summary report per release with go/no-go criteria

B) Report exists but no go/no-go criteria

C) Slide summary at release meeting

D) Verbal summary

E) Not communicated

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Recommend templated test summary tied to release approval.

SWE6_L2_06

ID: SWE6_L2_06

Level: L2

Criteria: GP 2.2.2 — Work-product requirements (defect management)

Identifies: Defect process weak at qualification

Stakeholder: QA, TE

Question: How are qualification-test defects managed and triaged?

Options:

A) Defects in tracker with severity, owner, SLA, root-cause field; weekly triage

B) Tracker used; no triage cadence

C) Defects in spreadsheet

D) Verbally tracked

E) No defect tracking

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Reference SUP.9 (out of scope); recommend root-cause field.

SWE6_L3_07

ID: SWE6_L3_07

Level: L3

Criteria: GP 3.2.4 — Monitor performance of defined process (information, not data)

Identifies: No process-improvement feedback loop

Stakeholder: ASR, QA, PM

Question: How is information from SWE.6 fed back into the organisational standard process?

Options:

A) Lessons-learned + KPIs reported to Process Group; standard process updated

B) Lessons-learned written, no link to standard process

C) Discussed in retro only

D) Captured in private notes

E) No feedback loop

Weights: 0, 2, 3, 4, 5

Recommendation Logic: PA 3.2 weakness; recommend a quarterly Process Group review channel.

---

Coverage Extension — 14 Additional Questions (SWE.1–SWE.6)

Derived from Aspice_document_concepts.md against the 42 questions above. Each item below
targets either (a) a base-practice outcome with no existing question, or (b) a generic
practice achievement (PA 2.1 / PA 2.2 / PA 3.1 / PA 3.2) not yet represented for that
process. Two are full outcome gaps: SWE.4 never asks about BP5 (summarize & communicate
unit-verification results), and SWE.5 never asks about BP7 (summarize & communicate
component/integration-verification results) — both are Outcome-level omissions in the
original 42.

SWE.1 — Software Requirements Analysis

SWE1_L1_08

ID: SWE1_L1_08

Level: L1

Criteria: SWE.1.BP5 — Ensure consistency & bidirectional traceability (SW-req ↔ system architecture)

Identifies: Missing allocation of SW requirements to system architecture elements

Stakeholder: SA, QA, ASR

Question: How is bidirectional traceability maintained between software requirements and the system architecture (i.e., allocation of SW requirements to system architecture elements)?

Options:

A) Tool-enforced allocation links, reviewed and audited each baseline

B) Allocation links exist but are not audited

C) Allocation documented in a spreadsheet, maintained manually

D) Allocation implicit / known only to individual engineers

E) No traceability to system architecture exists

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Distinct from SYS-req↔SW-req traceability (SWE1_L1_05) — BP5 covers two separate outcomes (O5, O6) and only O5 was previously asked. A gap here means SW requirements may not be correctly scoped to their allocated system-architecture element. Recommend extending the RTM with a system-architecture allocation column.

SWE1_L1_09

ID: SWE1_L1_09

Level: L1

Criteria: SWE.1.BP3 — Analyse SW requirements (interdependencies)

Identifies: Conflicting or circular requirement dependencies undetected until late

Stakeholder: SA, SD, QA

Question: How are dependencies and potential conflicts between software requirements identified and managed?

Options:

A) Dependencies explicitly modelled/tagged and conflict-checked at each baseline review

B) Dependencies documented but not systematically conflict-checked

C) Dependencies identified informally during design

D) Dependencies surface only when a defect/integration issue occurs

E) Not analysed

Weights: 0, 2, 3, 4, 5

Recommendation Logic: BP3 covers correctness, feasibility, and interdependencies; SWE1_L1_03 already covers feasibility, this closes the interdependency sub-aspect. Recommend a dependency/conflict tag in the requirements tool plus a conflict-check step in the review checklist.

SWE1_L2_10

ID: SWE1_L2_10

Level: L2

Criteria: GP 2.1.6 — Manage interfaces between involved parties (SWE.1)

Identifies: Poor coordination between requirements engineering and system engineering / other stakeholders

Stakeholder: SA, PM, TL

Question: How are interfaces between software requirements engineers and other involved parties (system engineering, safety, customer) coordinated for requirement changes?

Options:

A) Defined communication mechanism with assigned responsibilities and change-notification SLA

B) Communication mechanism exists but responsibilities not assigned

C) Coordination happens through periodic status meetings only

D) Coordination happens only when a conflict is discovered

E) No defined coordination mechanism

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Complements SWE1_L1_06 (one-time agreement) and SWE1_L2_07 (planning/KPIs); recommend a stakeholder communication matrix analogous to SWE5_L2_07's interface change board.

SWE1_L2_11

ID: SWE1_L2_11

Level: L2

Criteria: GP 2.2.1–2.2.3 — Work-product requirements, storage and control (SW requirements)

Identifies: Requirements work products not under configuration/status control

Stakeholder: QA, ASR

Question: How are the software requirement work products stored, versioned, and status-controlled (e.g., Under Work / Reviewed / Released)?

Options:

A) Versioned in requirements-management tool with a defined status workflow and baseline history

B) Versioned in tool but no formal status workflow

C) Stored in a shared drive/document, manually versioned

D) Stored locally by individual engineers

E) Not under any storage/version control

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Fills a PA 2.2 gap in SWE.1 — the existing SWE1 L2 question (SWE1_L2_07) only covers PA 2.1 planning. Recommend a CM-controlled requirements repository with baseline/status workflow (cf. SWE4_L2_07 pattern applied to requirements).

SWE.2 — Software Architectural Design

SWE2_L2_08

ID: SWE2_L2_08

Level: L2

Criteria: GP 2.1.3, GP 2.1.4 — Resource needs & qualification (SWE.2)

Identifies: Architects not trained/qualified on modelling method or tool; unavailable licences

Stakeholder: SA, TL, PM

Question: How is the competency of software architects (modelling method/tool skills) and the availability of architecture tooling (e.g., EA/Cameo licences) ensured?

Options:

A) Defined competency requirement, training/mentoring plan, and licence/tool availability tracked

B) Training available but not tracked; tool availability assumed

C) New architects learn on the job, no formal plan

D) Competency/tooling addressed only when a problem arises

E) No defined approach

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Fills the PA 2.1 "persons prepared for their responsibilities" achievement (GP 2.1.4), absent everywhere else in the bank; recommend a role-based training plan and licence-tracking process.

SWE2_L2_09

ID: SWE2_L2_09

Level: L2

Criteria: GP 2.1.6 — Manage interfaces between involved parties (SWE.2)

Identifies: Architecture changes not propagated to detailed-design / integration teams

Stakeholder: SA, TL, PM

Question: When the software architecture changes after initial communication, how are affected detailed-design and integration teams notified and re-aligned?

Options:

A) Change-notification mechanism with defined recipients and acknowledgement tracking

B) Notification sent, but acknowledgement not tracked

C) Announced only in the next regular meeting

D) Discovered by affected teams when inconsistencies appear

E) No mechanism

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Distinct from the one-time communication event in SWE2_L1_06 — this targets ongoing change coordination once the architecture evolves. Recommend an architecture change board, mirroring SWE5_L2_07's ICB pattern.

SWE2_L3_10

ID: SWE2_L3_10

Level: L3

Criteria: GP 3.1.2, GP 3.1.3 — Required competencies & resources for the standard process (SWE.2)

Identifies: No organisation-level role/competency definition for the architecture role

Stakeholder: ASR, PM, SA

Question: Does the organisation maintain a defined role description (required competencies, responsibilities) and standard tooling/infrastructure for the software architect role?

Options:

A) Documented role description and standard tooling maintained and referenced by projects

B) Role description exists but tooling/infrastructure not standardised

C) Informal, unwritten expectations for the role

D) Role description exists only for other roles (not architect)

E) No role description or standard infrastructure defined

Weights: 0, 2, 3, 4, 5

Recommendation Logic: PA 3.1 organisational-maturity check — approximated here from a single respondent's session, per the documented tool limitation (Section 7.4 note in concepts doc); recommend establishing a role-description template at Process Group level.

SWE.3 — Software Detailed Design and Unit Construction

SWE3_L2_08

ID: SWE3_L2_08

Level: L2

Criteria: GP 2.2.2, GP 2.2.3 — Storage and control of work products (source code & detailed design)

Identifies: Source code / detailed design not under proper configuration control

Stakeholder: QA, SD, ASR

Question: How are source code and detailed-design work products identified, versioned, and controlled during development?

Options:

A) Version-controlled with branching/baseline policy and a defined status model (e.g., Under Work/Reviewed/Released)

B) Version-controlled, but no defined status model

C) Version-controlled only for source code, not detailed design

D) Ad-hoc use of version control, no policy

E) Not under version/configuration control

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Distinct from SWE3_L2_06 (defect/rework monitoring, GP 2.1.5) — this fills the PA 2.2 work-product-control gap for SWE.3. Recommend a CM branching/baseline policy covering both code and design artefacts.

SWE.4 — Software Unit Verification

SWE4_L1_08

ID: SWE4_L1_08

Level: L1

Criteria: SWE.4.BP5 — Summarize and communicate results

Identifies: Unit-verification results not summarised/communicated to affected parties

Stakeholder: SD, TE, TL

Question: How are software unit-verification results (pass/fail, coverage, static-analysis findings) summarised and communicated to affected parties?

Options:

A) Automated summary report generated per build/release and distributed to affected parties

B) Summary report generated but only on request

C) Results visible only inside the test-management tool, not actively communicated

D) Communicated verbally / informally

E) Not summarised or communicated

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Closes a full outcome gap — BP5/Outcome 5 was previously unassessed for SWE.4 across all 42 questions. Recommend a build-level unit-verification summary report distributed to development and QA.

SWE4_L3_09

ID: SWE4_L3_09

Level: L3

Criteria: GP 3.1.1, GP 3.1.4 — Standard process & monitoring (SWE.4)

Identifies: Unit-verification approach/tooling not standardised or monitored across projects

Stakeholder: ASR, QA, PM

Question: Is there an organisation-wide standard for unit-verification methods/tooling (static-analysis rulesets, coverage thresholds), and is its effectiveness monitored?

Options:

A) Standard method/tooling defined, tailoring guideline available, effectiveness monitored and fed back

B) Standard defined, but effectiveness not monitored

C) Each project chooses its own tooling/thresholds independently

D) Standard exists informally, not documented

E) No organisational standard for unit verification

Weights: 0, 2, 3, 4, 5

Recommendation Logic: SWE.4 previously had no L3 question; parallels SWE6_L3_07's feedback-loop pattern applied to unit verification. Recommend a Process Group review of unit-verification effectiveness metrics.

SWE.5 — Software Component Verification and Integration Verification

SWE5_L1_08

ID: SWE5_L1_08

Level: L1

Criteria: SWE.5.BP7 — Summarize and communicate results

Identifies: Component/integration verification results not summarised/communicated

Stakeholder: TE, SA, PM

Question: How are software component-verification and integration-verification results summarised and communicated to affected parties?

Options:

A) Versioned summary report per integration baseline with pass/fail overview, distributed to affected parties

B) Summary report exists, distributed only on request

C) Results visible in test tool only, not actively communicated

D) Communicated verbally in status meetings

E) Not summarised or communicated

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Closes a full outcome gap — BP7/Outcome 8 was previously unassessed for SWE.5 across all 42 questions. Recommend an integration-baseline summary report as a release-readiness input to SWE.6.

SWE5_L2_09

ID: SWE5_L2_09

Level: L2

Criteria: GP 2.2.2, GP 2.2.3 — Storage and control of work products (component/integration verification reports)

Identifies: Integration-verification reports not under configuration control

Stakeholder: QA

Question: How are component-verification and integration-verification reports stored, versioned, and controlled?

Options:

A) Versioned in CM with a defined status workflow and reviewer sign-off

B) Versioned only, no status workflow

C) Stored on a shared drive, no versioning

D) Stored locally by individual testers

E) Not formally stored

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Fills the PA 2.2 gap for SWE.5 — the existing SWE5 GP question (SWE5_L2_07) covers only PA 2.1 interface coordination. Mirrors the SWE4_L2_07 pattern applied to the integration-verification artefact set.

SWE5_L3_10

ID: SWE5_L3_10

Level: L3

Criteria: GP 3.1.1 — Standard process (integration strategy)

Identifies: No organisation-wide standard for integration approach

Stakeholder: ASR, SA, PM

Question: Does the organisation define a standard integration strategy (e.g., stepwise vs. continuous integration, environments to be used) that projects tailor from?

Options:

A) Documented standard integration strategy with tailoring guideline, applied and reviewed

B) Standard exists but tailoring is undocumented

C) Each project defines its own integration strategy independently

D) Informal convention, not documented

E) No organisational standard

Weights: 0, 2, 3, 4, 5

Recommendation Logic: SWE.5 previously had no L3 question; PA 3.1 organisational-maturity check. Recommend a Process Group-maintained integration-strategy template.

SWE.6 — Software Verification

SWE6_L2_08

ID: SWE6_L2_08

Level: L2

Criteria: GP 2.1.1, GP 2.1.2, GP 2.1.3 — Strategy, planning and resource readiness for SWE.6

Identifies: Qualification-verification activity not planned/resourced ahead of release

Stakeholder: PM, TE, TL

Question: How is the SWE.6 qualification-verification activity planned and resourced ahead of a release (schedule, staffing, target-environment availability)?

Options:

A) Documented plan with milestones, staffing, and environment booking confirmed ahead of release

B) Plan exists but staffing/environment not confirmed in advance

C) Planned informally per release, no documented milestones

D) Planned reactively once development is "done"

E) No planning for qualification verification

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Fills the PA 2.1 gap for SWE.6 — the existing SWE6 GP questions cover only PA 2.2 (defect management, SWE6_L2_06) and PA 3.2 (feedback loop, SWE6_L3_07), never PA 2.1 planning. Recommend a release-readiness checklist including qualification-environment booking (cf. SWE4_L2_06 pattern applied to the qualification stage).

---

Coverage Extension, Batch 2 — 4 Additional Questions (56 → 60)

These close the remaining process-attribute gaps left after Batch 1: SWE.1 had no L3
question at all (0 of 6 processes' L3 coverage was still missing for SWE.1); SWE.2 and
SWE.3 had no PA 2.1 "strategy & planning" question for their own process (only for
monitoring/resourcing sub-aspects); and SWE.6's L3 coverage addressed only GP 3.2.4
(process monitoring/feedback) but never GP 3.1.1 (establishing the standard process itself).

SWE.1 — Software Requirements Analysis

SWE1_L3_12

ID: SWE1_L3_12

Level: L3

Criteria: GP 3.1.1, GP 3.1.2 — Standard process & required competencies (SWE.1)

Identifies: No organisation-wide standard for requirements-engineering methodology/roles

Stakeholder: ASR, PM, SA

Question: Does the organisation maintain a standard requirements-engineering process (templates, tailoring guideline) and a defined role/competency description for the requirements-engineer role?

Options:

A) Documented standard RE process + tailoring guideline + role/competency description, maintained and referenced by projects

B) Standard process exists, but role/competency description is missing

C) A requirements template exists informally, not maintained centrally

D) Each project defines its own RE approach independently

E) No organisational standard or role description exists

Weights: 0, 2, 3, 4, 5

Recommendation Logic: SWE.1 had no L3 question in the original 42 or in Batch 1 — this is the sole remaining organisational-maturity gap for the process. PA 3.1 check, paralleling SWE2_L3_10's pattern for the architecture role. Recommend establishing an RE process template + role description at Process Group level.

SWE.2 — Software Architectural Design

SWE2_L2_11

ID: SWE2_L2_11

Level: L2

Criteria: GP 2.1.1, GP 2.1.2 — Strategy & planning for SWE.2

Identifies: Architecture design activity not planned against objectives/milestones

Stakeholder: PM, SA

Question: How is the SWE.2 architecture design activity planned and monitored at project level (objectives, milestones, schedule)?

Options:

A) Documented architecture design plan with objectives/milestones, reviewed and adjusted regularly

B) Plan exists but not actively monitored/adjusted

C) Milestones exist only in the overall project schedule, not architecture-specific

D) Planned ad-hoc per sprint

E) No plan for the architecture design activity

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Fills the PA 2.1 "strategy and planning" gap for SWE.2 — existing SWE2 L2 questions cover competency (SWE2_L2_08), interface/change coordination (SWE2_L2_09), and work-product review (SWE2_L2_07), but not planning of the design activity itself. Mirrors the SWE1_L2_07 pattern, applied to the architecture process.

SWE.3 — Software Detailed Design and Unit Construction

SWE3_L2_09

ID: SWE3_L2_09

Level: L2

Criteria: GP 2.1.1, GP 2.1.2 — Strategy & planning for SWE.3

Identifies: Detailed design & unit construction activity not planned against objectives/staffing

Stakeholder: PM, TL, SD

Question: How is the SWE.3 detailed design and unit construction activity planned (staffing, schedule, objectives per component)?

Options:

A) Documented plan with per-component staffing/schedule, objectives tracked and adjusted

B) Plan exists but not tracked against actuals

C) Only covered by the general sprint backlog, no dedicated plan

D) Planned informally by the team lead

E) No planning for the detailed design/construction activity

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Fills the PA 2.1 "strategy and planning" gap for SWE.3 — existing SWE3 L2 questions cover monitoring (SWE3_L2_06, GP 2.1.5) and CM control (SWE3_L2_08, GP 2.2), but not upfront planning of the activity itself.

SWE.6 — Software Verification

SWE6_L3_09

ID: SWE6_L3_09

Level: L3

Criteria: GP 3.1.1 — Standard process (qualification-test strategy)

Identifies: No organisation-wide standard qualification-test methodology

Stakeholder: ASR, TE, PM

Question: Does the organisation maintain a standard qualification-test methodology/template (e.g., technique-selection guideline, standard test-environment setup) that projects tailor from?

Options:

A) Documented standard methodology/template with tailoring guideline, applied and reviewed across projects

B) Standard exists but the tailoring guideline is missing

C) Each project defines its own qualification-test methodology independently

D) Informal convention, not documented

E) No organisational standard

Weights: 0, 2, 3, 4, 5

Recommendation Logic: Distinct from SWE6_L3_07 (GP 3.2.4 — monitoring/feedback loop of the already-deployed process) — this addresses GP 3.1.1, the prior step of establishing a standard process in the first place. Closes the last PA 3.1 gap for SWE.6, paralleling SWE4_L3_09/SWE5_L3_10.