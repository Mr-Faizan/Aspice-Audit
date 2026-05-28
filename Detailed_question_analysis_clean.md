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