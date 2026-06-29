"""
Seed script: inserts all ASPICE SWE.1–SWE.6 audit questions and options.
Run inside the backend container:
  python app/seed_questions.py
"""
from datetime import datetime, timezone

from sqlmodel import Session, select
from app.core.db import engine
from app.models import AuditQuestion, AuditOption, ProcessEnum

# Maps old "SWE.N" process strings to ProcessEnum values
PROCESS_MAP = {
    "SWE.1": ProcessEnum.SWE1,
    "SWE.2": ProcessEnum.SWE2,
    "SWE.3": ProcessEnum.SWE3,
    "SWE.4": ProcessEnum.SWE4,
    "SWE.5": ProcessEnum.SWE5,
    "SWE.6": ProcessEnum.SWE6,
}

# Maps short stakeholder codes to StakeholderRoleEnum string values
STAKEHOLDER_MAP = {
    "SA": "software_architect",
    "SD": "software_developer",
    "QA": "qa_engineer",
    "PM": "project_manager",
    "TE": "test_engineer",
    "TL": "team_lead",
    "ASR": "aspice_assessor",
}


def extract_base_practice_id(criteria: str) -> str:
    """Pull the BP/GP code from the criteria string, e.g. 'SWE.1.BP1 — ...' → 'SWE.1.BP1'."""
    return criteria.split(" — ")[0].split(",")[0].strip()

# ---------------------------------------------------------------------------
# Question data
# ---------------------------------------------------------------------------

QUESTIONS = [
    # -----------------------------------------------------------------------
    # SWE.1 — Software Requirements Analysis
    # -----------------------------------------------------------------------
    {
        "question_code": "SWE1_L1_01",
        "process": "SWE.1",
        "level": "L1",
        "criteria": "SWE.1.BP1 — Specify SW requirements (verifiability, unambiguity)",
        "identifies": "Weak requirement quality, ambiguity, untestable SW requirements",
        "stakeholders": ["SA", "SD", "QA"],
        "question_text": "How are software requirements specified for the current release?",
        "recommendation_logic": "High weight ⇒ recommend a requirement-specification template aligned with IEEE 29148 + tooling audit (DOORS/Polarion/Jama).",
        "options": [
            {"label": "A", "option_text": "Each requirement is uniquely identified, atomic, verifiable and references its source", "weight": 0},
            {"label": "B", "option_text": "Requirements are uniquely identified but verifiability criteria are missing for some", "weight": 2},
            {"label": "C", "option_text": "Requirements exist as free-text paragraphs without unique IDs", "weight": 3},
            {"label": "D", "option_text": "Requirements are partially captured in slides/e-mails", "weight": 4},
            {"label": "E", "option_text": "No formal SW requirements set exists", "weight": 5},
        ],
    },
    {
        "question_code": "SWE1_L1_02",
        "process": "SWE.1",
        "level": "L1",
        "criteria": "SWE.1.BP2 — Structure SW requirements",
        "identifies": "Missing prioritisation / categorisation, scope-creep risk",
        "stakeholders": ["PM", "SA"],
        "question_text": "How are SW requirements categorised and prioritised?",
        "recommendation_logic": "Recommend introducing a categorisation scheme + MoSCoW/RICE prioritisation linked to MAN.3 (out of scope but referenced).",
        "options": [
            {"label": "A", "option_text": "Categorised (functional/non-functional/safety/security) and prioritised against release plan", "weight": 0},
            {"label": "B", "option_text": "Categorised only", "weight": 2},
            {"label": "C", "option_text": "Prioritised only", "weight": 2},
            {"label": "D", "option_text": "Done ad-hoc per request", "weight": 4},
            {"label": "E", "option_text": "Not categorised or prioritised", "weight": 5},
        ],
    },
    {
        "question_code": "SWE1_L1_03",
        "process": "SWE.1",
        "level": "L1",
        "criteria": "SWE.1.BP3 — Analyse SW requirements (correctness, technical feasibility)",
        "identifies": "Latent feasibility risk, late re-work",
        "stakeholders": ["SA", "SD"],
        "question_text": "How is the technical feasibility of new SW requirements analysed before they are baselined?",
        "recommendation_logic": "Recommend a feasibility-review checklist gated on requirement baselining.",
        "options": [
            {"label": "A", "option_text": "Formal feasibility review with architect & developer sign-off", "weight": 0},
            {"label": "B", "option_text": "Informal feasibility check by architect only", "weight": 2},
            {"label": "C", "option_text": "Feasibility judged during implementation", "weight": 4},
            {"label": "D", "option_text": "Feasibility never explicitly checked", "weight": 5},
            {"label": "E", "option_text": "Unknown / no defined approach", "weight": 5},
        ],
    },
    {
        "question_code": "SWE1_L1_04",
        "process": "SWE.1",
        "level": "L1",
        "criteria": "SWE.1.BP4 — Analyse impact on operating environment",
        "identifies": "Missed timing / ODD / resource impact",
        "stakeholders": ["SA", "SD"],
        "question_text": "When SW requirements affect timing, memory, or operating-environment behaviour, how is the impact captured?",
        "recommendation_logic": "Recommend introducing impact-analysis fields in the requirement template; cross-link to non-functional verification in SWE.6.",
        "options": [
            {"label": "A", "option_text": "Documented impact analysis linked to each affected requirement", "weight": 0},
            {"label": "B", "option_text": "Captured in design notes only", "weight": 2},
            {"label": "C", "option_text": "Discussed verbally in reviews", "weight": 3},
            {"label": "D", "option_text": "Not analysed unless a defect is found", "weight": 4},
            {"label": "E", "option_text": "No process", "weight": 5},
        ],
    },
    {
        "question_code": "SWE1_L1_05",
        "process": "SWE.1",
        "level": "L1",
        "criteria": "SWE.1.BP5 — Ensure consistency & bidirectional traceability (SYS-req ↔ SW-req ↔ SYS-arch)",
        "identifies": "Broken bidirectional traceability — top assessor finding",
        "stakeholders": ["SA", "QA", "ASR"],
        "question_text": "What is the current state of bidirectional traceability between system requirements and software requirements?",
        "recommendation_logic": "High signal: recommend RTM/OSLC tooling audit and a SUP.10 change-impact review procedure (referenced, not in scope).",
        "options": [
            {"label": "A", "option_text": "Tool-enforced bidirectional links, audited every release", "weight": 0},
            {"label": "B", "option_text": "Bidirectional links exist but coverage is partial", "weight": 2},
            {"label": "C", "option_text": "Only forward links (SYS→SW) exist", "weight": 3},
            {"label": "D", "option_text": "Traceability is maintained in spreadsheets", "weight": 4},
            {"label": "E", "option_text": "No traceability data", "weight": 5},
        ],
    },
    {
        "question_code": "SWE1_L1_06",
        "process": "SWE.1",
        "level": "L1",
        "criteria": "SWE.1.BP6 — Communicate agreed SW requirements & impact",
        "identifies": "Lack of agreement → late churn",
        "stakeholders": ["PM", "SA", "TL"],
        "question_text": "How is agreement on the SW requirements baseline reached and recorded?",
        "recommendation_logic": "Recommend introducing a lightweight \"Requirements Agreement Record\" gate.",
        "options": [
            {"label": "A", "option_text": "Formal review meeting with signed-off minutes per release", "weight": 0},
            {"label": "B", "option_text": "Review meeting without recorded sign-off", "weight": 2},
            {"label": "C", "option_text": "E-mail confirmation only", "weight": 3},
            {"label": "D", "option_text": "Implicit agreement, no record", "weight": 4},
            {"label": "E", "option_text": "No agreement step", "weight": 5},
        ],
    },
    {
        "question_code": "SWE1_L2_07",
        "process": "SWE.1",
        "level": "L2",
        "criteria": "GP 2.1.1, GP 2.1.2 — Performance objectives & planning for SWE.1",
        "identifies": "Missing/weak strategy for the requirements process",
        "stakeholders": ["PM", "QA"],
        "question_text": "How is the SWE.1 process planned and monitored at project level?",
        "recommendation_logic": "Indicates PA 2.1 weakness; recommend a requirements KPI dashboard.",
        "options": [
            {"label": "A", "option_text": "Documented requirements-engineering plan with KPIs (e.g., review backlog, churn) reviewed monthly", "weight": 0},
            {"label": "B", "option_text": "Plan exists but KPIs are not tracked", "weight": 2},
            {"label": "C", "option_text": "Activities scheduled in MS-Project only", "weight": 3},
            {"label": "D", "option_text": "Planned ad-hoc per sprint", "weight": 4},
            {"label": "E", "option_text": "No plan", "weight": 5},
        ],
    },
    # -----------------------------------------------------------------------
    # SWE.2 — Software Architectural Design
    # -----------------------------------------------------------------------
    {
        "question_code": "SWE2_L1_01",
        "process": "SWE.2",
        "level": "L1",
        "criteria": "SWE.2.BP1 — Specify static aspects of architecture",
        "identifies": "Missing decomposition / structural views",
        "stakeholders": ["SA"],
        "question_text": "How is the static structure of the SW architecture documented?",
        "recommendation_logic": "Recommend a model-based architecture in EA/Cameo; flag tool break to traceability.",
        "options": [
            {"label": "A", "option_text": "Hierarchical component model with explicit interfaces, in a modelling tool (UML/SysML/EA)", "weight": 0},
            {"label": "B", "option_text": "Block diagrams in modelling tool, no interface model", "weight": 2},
            {"label": "C", "option_text": "PowerPoint diagrams", "weight": 3},
            {"label": "D", "option_text": "Textual description only", "weight": 4},
            {"label": "E", "option_text": "Not documented", "weight": 5},
        ],
    },
    {
        "question_code": "SWE2_L1_02",
        "process": "SWE.2",
        "level": "L1",
        "criteria": "SWE.2.BP2 — Specify dynamic aspects (timing, sequences, state)",
        "identifies": "Hidden timing/concurrency defects",
        "stakeholders": ["SA", "SD"],
        "question_text": "How are dynamic aspects (timing, sequencing, state) specified for the architecture?",
        "recommendation_logic": "Recommend timing-budget table; pair with SWE.5 integration tests.",
        "options": [
            {"label": "A", "option_text": "Sequence + state diagrams + timing budgets per component", "weight": 0},
            {"label": "B", "option_text": "Sequence diagrams only", "weight": 2},
            {"label": "C", "option_text": "Narrative timing notes", "weight": 3},
            {"label": "D", "option_text": "Implicit, decided during coding", "weight": 4},
            {"label": "E", "option_text": "Not specified", "weight": 5},
        ],
    },
    {
        "question_code": "SWE2_L1_03",
        "process": "SWE.2",
        "level": "L1",
        "criteria": "SWE.2.BP3 — Analyse architecture, justify chosen design (PAM 4.0 replaces former \"evaluate alternatives\" BP)",
        "identifies": "Unjustified architecture, hidden trade-offs",
        "stakeholders": ["SA", "ASR"],
        "question_text": "How is the chosen architecture justified against alternatives and quality criteria (modularity, reliability, security)?",
        "recommendation_logic": "High signal: recommend architecture-decision-record (ADR) practice.",
        "options": [
            {"label": "A", "option_text": "Documented trade-off analysis with rationale recorded per decision", "weight": 0},
            {"label": "B", "option_text": "Decision log with brief rationale", "weight": 2},
            {"label": "C", "option_text": "Verbal discussion in design review", "weight": 3},
            {"label": "D", "option_text": "Not justified, \"as-is\"", "weight": 4},
            {"label": "E", "option_text": "Decision-maker unknown", "weight": 5},
        ],
    },
    {
        "question_code": "SWE2_L1_04",
        "process": "SWE.2",
        "level": "L1",
        "criteria": "SWE.2.BP3 — interfaces & resource consumption",
        "identifies": "Interface ambiguity, resource overruns at HIL/qualification",
        "stakeholders": ["SA", "SD"],
        "question_text": "How are interfaces and resource-consumption objectives (RAM/ROM/CPU/bandwidth) defined for SW components?",
        "recommendation_logic": "Recommend interface contracts + per-component budgets; verify with static analysis (SWE.4).",
        "options": [
            {"label": "A", "option_text": "Each interface fully typed; RAM/ROM/CPU budgets per component", "weight": 0},
            {"label": "B", "option_text": "Interfaces typed; no resource budgets", "weight": 2},
            {"label": "C", "option_text": "Resource budgets only at SW level (not per component)", "weight": 3},
            {"label": "D", "option_text": "Defined only when problems arise", "weight": 4},
            {"label": "E", "option_text": "Not defined", "weight": 5},
        ],
    },
    {
        "question_code": "SWE2_L1_05",
        "process": "SWE.2",
        "level": "L1",
        "criteria": "SWE.2.BP4 — Consistency & bidirectional traceability (SW-req ↔ SW-arch)",
        "identifies": "Architecture/requirement drift",
        "stakeholders": ["SA", "QA", "ASR"],
        "question_text": "How is bidirectional traceability maintained between SW requirements and architectural elements?",
        "recommendation_logic": "Recommend OSLC-style linking; tie to SWE.1 traceability question to detect compounded weakness.",
        "options": [
            {"label": "A", "option_text": "Tool-enforced (allocation column / OSLC link) and reviewed each baseline", "weight": 0},
            {"label": "B", "option_text": "Maintained but not periodically audited", "weight": 2},
            {"label": "C", "option_text": "Manual matrix in spreadsheet", "weight": 3},
            {"label": "D", "option_text": "Allocation is implicit", "weight": 4},
            {"label": "E", "option_text": "No traceability", "weight": 5},
        ],
    },
    {
        "question_code": "SWE2_L1_06",
        "process": "SWE.2",
        "level": "L1",
        "criteria": "SWE.2.BP5 — Communicate agreed architecture",
        "identifies": "Architecture not internalised by team",
        "stakeholders": ["SA", "TL"],
        "question_text": "How is the agreed architecture communicated and made available to development and test teams?",
        "recommendation_logic": "Recommend onboarding workshop + searchable architecture site.",
        "options": [
            {"label": "A", "option_text": "Published in the team wiki + walk-through workshop with attendance log", "weight": 0},
            {"label": "B", "option_text": "Published in wiki only", "weight": 2},
            {"label": "C", "option_text": "Sent by e-mail", "weight": 3},
            {"label": "D", "option_text": "Available on request", "weight": 4},
            {"label": "E", "option_text": "Not communicated", "weight": 5},
        ],
    },
    {
        "question_code": "SWE2_L2_07",
        "process": "SWE.2",
        "level": "L2",
        "criteria": "GP 2.2.1, GP 2.2.4 — Work-product requirements & review for architecture artefacts",
        "identifies": "Architecture artefacts not reviewed against criteria",
        "stakeholders": ["QA", "ASR"],
        "question_text": "How are architecture work products (model, ADRs, interface specs) reviewed and approved?",
        "recommendation_logic": "Indicates PA 2.2 weakness; recommend SUP.1-style work-product review template.",
        "options": [
            {"label": "A", "option_text": "Defined review checklist + approver role + review record per baseline", "weight": 0},
            {"label": "B", "option_text": "Review checklist but no approver role", "weight": 2},
            {"label": "C", "option_text": "Reviews held without checklist", "weight": 3},
            {"label": "D", "option_text": "Reviews held only when issues escalate", "weight": 4},
            {"label": "E", "option_text": "No reviews", "weight": 5},
        ],
    },
    # -----------------------------------------------------------------------
    # SWE.3 — Software Detailed Design and Unit Construction
    # -----------------------------------------------------------------------
    {
        "question_code": "SWE3_L1_01",
        "process": "SWE.3",
        "level": "L1",
        "criteria": "SWE.3.BP1 — Specify static aspects of detailed design",
        "identifies": "Skipping detailed design, \"code-is-design\" antipattern",
        "stakeholders": ["SA", "SD"],
        "question_text": "How is the static detailed design of software units captured?",
        "recommendation_logic": "Recommend keeping design synchronised via code-from-model or model-from-code.",
        "options": [
            {"label": "A", "option_text": "Class/data structure model in tool, generated from architecture", "weight": 0},
            {"label": "B", "option_text": "Diagrams in modelling tool, manually maintained", "weight": 2},
            {"label": "C", "option_text": "Text-and-code-comments only", "weight": 3},
            {"label": "D", "option_text": "Comments in source code", "weight": 4},
            {"label": "E", "option_text": "No detailed design", "weight": 5},
        ],
    },
    {
        "question_code": "SWE3_L1_02",
        "process": "SWE.3",
        "level": "L1",
        "criteria": "SWE.3.BP2 — Specify dynamic aspects of detailed design",
        "identifies": "Hidden control-flow / state defects",
        "stakeholders": ["SD", "SA"],
        "question_text": "How are state machines, control flows, and unit interactions described?",
        "recommendation_logic": "Recommend state-chart coverage for safety-critical paths.",
        "options": [
            {"label": "A", "option_text": "State/sequence diagrams per non-trivial unit", "weight": 0},
            {"label": "B", "option_text": "Diagrams only for safety-critical units", "weight": 2},
            {"label": "C", "option_text": "Narrative description", "weight": 3},
            {"label": "D", "option_text": "Discovered during coding", "weight": 4},
            {"label": "E", "option_text": "Not described", "weight": 5},
        ],
    },
    {
        "question_code": "SWE3_L1_03",
        "process": "SWE.3",
        "level": "L1",
        "criteria": "SWE.3.BP3 — Develop software units (coding standard adherence)",
        "identifies": "Coding-standard violations, MISRA gaps",
        "stakeholders": ["SD", "QA"],
        "question_text": "How are coding standards (e.g., MISRA C/C++, AUTOSAR C++14) enforced during unit construction?",
        "recommendation_logic": "High signal: recommend Axivion/Polyspace/Coverity gate; flag SWE.4 static-analysis question for re-check.",
        "options": [
            {"label": "A", "option_text": "Pre-commit check + CI gate blocks merges on standard violations", "weight": 0},
            {"label": "B", "option_text": "CI gate runs but does not block merges", "weight": 2},
            {"label": "C", "option_text": "Periodic audit by QA", "weight": 3},
            {"label": "D", "option_text": "Standard exists but is not enforced", "weight": 4},
            {"label": "E", "option_text": "No coding standard adopted", "weight": 5},
        ],
    },
    {
        "question_code": "SWE3_L1_04",
        "process": "SWE.3",
        "level": "L1",
        "criteria": "SWE.3.BP4 — Consistency & bidirectional traceability (SW-req ↔ arch ↔ detailed design ↔ units)",
        "identifies": "Multi-hop traceability gap",
        "stakeholders": ["SA", "QA", "ASR"],
        "question_text": "What is the state of traceability from architecture → detailed design → source units?",
        "recommendation_logic": "Strongest predictor of CL2 failure across SWE.3; recommend OSLC link consolidation.",
        "options": [
            {"label": "A", "option_text": "End-to-end tool-enforced, audited each release", "weight": 0},
            {"label": "B", "option_text": "Forward links complete; reverse links partial", "weight": 2},
            {"label": "C", "option_text": "Spreadsheet only", "weight": 3},
            {"label": "D", "option_text": "Traceability stops at design level", "weight": 4},
            {"label": "E", "option_text": "No links", "weight": 5},
        ],
    },
    {
        "question_code": "SWE3_L1_05",
        "process": "SWE.3",
        "level": "L1",
        "criteria": "SWE.3.BP5 — Communicate agreed detailed design and units",
        "identifies": "Knowledge silo, single-point-of-failure",
        "stakeholders": ["SD", "TL"],
        "question_text": "How are agreed detailed design and developed units made available to peers and testers?",
        "recommendation_logic": "Recommend mandatory peer review and shared design index.",
        "options": [
            {"label": "A", "option_text": "Reviewed pull requests + design documented in shared repo", "weight": 0},
            {"label": "B", "option_text": "Code committed, design in shared repo", "weight": 2},
            {"label": "C", "option_text": "Code only, design private to developer", "weight": 3},
            {"label": "D", "option_text": "Code on local branches, no design", "weight": 4},
            {"label": "E", "option_text": "Knowledge held by one developer", "weight": 5},
        ],
    },
    {
        "question_code": "SWE3_L2_06",
        "process": "SWE.3",
        "level": "L2",
        "criteria": "GP 2.1.5 — Monitor & adjust process (defect/rework rates per unit)",
        "identifies": "No control loop for code quality",
        "stakeholders": ["TL", "QA", "PM"],
        "question_text": "How is the SWE.3 process monitored at project level (e.g., rework, defect density per unit)?",
        "recommendation_logic": "PA 2.1 weakness; recommend defect-density dashboard and threshold-based escalation.",
        "options": [
            {"label": "A", "option_text": "Defect-density and rework metrics tracked weekly with thresholds", "weight": 0},
            {"label": "B", "option_text": "Metrics tracked monthly, no thresholds", "weight": 2},
            {"label": "C", "option_text": "Metrics gathered only for assessments", "weight": 3},
            {"label": "D", "option_text": "No monitoring beyond burndown", "weight": 4},
            {"label": "E", "option_text": "Not monitored", "weight": 5},
        ],
    },
    {
        "question_code": "SWE3_L3_07",
        "process": "SWE.3",
        "level": "L3",
        "criteria": "GP 3.1.1, GP 3.1.4 — Standard process & tailoring guidelines",
        "identifies": "Project-specific drift from organisational standard",
        "stakeholders": ["ASR", "QA", "PM"],
        "question_text": "How is the organisation's standard SWE.3 process tailored for this project?",
        "recommendation_logic": "Note: option C is mid-risk because lack of tailoring often hides cargo-cult adoption; recommend formal tailoring record.",
        "options": [
            {"label": "A", "option_text": "Tailoring documented against tailoring guidelines, reviewed by Process Group", "weight": 0},
            {"label": "B", "option_text": "Tailoring documented, not reviewed", "weight": 2},
            {"label": "C", "option_text": "Project follows standard process verbatim, no tailoring", "weight": 3},
            {"label": "D", "option_text": "Tailoring done informally", "weight": 4},
            {"label": "E", "option_text": "No standard process exists", "weight": 5},
        ],
    },
    # -----------------------------------------------------------------------
    # SWE.4 — Software Unit Verification
    # -----------------------------------------------------------------------
    {
        "question_code": "SWE4_L1_01",
        "process": "SWE.4",
        "level": "L1",
        "criteria": "SWE.4.BP1 — Specify unit-verification measures (tactic)",
        "identifies": "Missing verification tactic",
        "stakeholders": ["TE", "SD"],
        "question_text": "How are unit-verification measures (test cases, static analysis, coverage goals) specified?",
        "recommendation_logic": "Recommend a unit-verification specification template with derivation columns.",
        "options": [
            {"label": "A", "option_text": "Documented per component, derived from detailed design and non-functional reqs", "weight": 0},
            {"label": "B", "option_text": "Documented but not derived from non-functional reqs", "weight": 2},
            {"label": "C", "option_text": "Test cases only, no static-analysis measures", "weight": 3},
            {"label": "D", "option_text": "Specified ad-hoc", "weight": 4},
            {"label": "E", "option_text": "Not specified", "weight": 5},
        ],
    },
    {
        "question_code": "SWE4_L1_02",
        "process": "SWE.4",
        "level": "L1",
        "criteria": "SWE.4.BP2 — Select verification measures incl. regression",
        "identifies": "Insufficient regression coverage",
        "stakeholders": ["TE"],
        "question_text": "How are verification measures selected per release, including regression?",
        "recommendation_logic": "High signal for late-stage defects; recommend change-impact-driven regression.",
        "options": [
            {"label": "A", "option_text": "Selection rules documented and applied per release; regression set auto-derived from change-impact", "weight": 0},
            {"label": "B", "option_text": "Regression decided manually each release", "weight": 2},
            {"label": "C", "option_text": "Always run all unit tests", "weight": 2},
            {"label": "D", "option_text": "Regression decided only when defects appear", "weight": 4},
            {"label": "E", "option_text": "No selection mechanism", "weight": 5},
        ],
    },
    {
        "question_code": "SWE4_L1_03",
        "process": "SWE.4",
        "level": "L1",
        "criteria": "SWE.4.BP3 — Verify (static + dynamic)",
        "identifies": "Weak static analysis",
        "stakeholders": ["SD", "QA"],
        "question_text": "How is static analysis performed on software units?",
        "recommendation_logic": "Reinforces SWE3_L1_03; recommend severity-based blocking gate.",
        "options": [
            {"label": "A", "option_text": "Tool integrated in CI; zero high-severity findings policy", "weight": 0},
            {"label": "B", "option_text": "Tool integrated in CI; findings tracked but not blocking", "weight": 2},
            {"label": "C", "option_text": "Manual code reviews only", "weight": 3},
            {"label": "D", "option_text": "Static analysis runs only before milestones", "weight": 4},
            {"label": "E", "option_text": "Not performed", "weight": 5},
        ],
    },
    {
        "question_code": "SWE4_L1_04",
        "process": "SWE.4",
        "level": "L1",
        "criteria": "SWE.4.BP3 — Test SW units & record results (coverage)",
        "identifies": "Inadequate structural coverage",
        "stakeholders": ["TE", "SD"],
        "question_text": "What unit-test coverage criteria are applied for non-safety code?",
        "recommendation_logic": "Recommend MC/DC for ASIL B+ paths; align thresholds with ISO 26262 (referenced).",
        "options": [
            {"label": "A", "option_text": "Statement + branch coverage with documented threshold (e.g., ≥ 90 % branch)", "weight": 0},
            {"label": "B", "option_text": "Statement coverage threshold only", "weight": 2},
            {"label": "C", "option_text": "Coverage measured but no threshold", "weight": 3},
            {"label": "D", "option_text": "Coverage measured ad-hoc", "weight": 4},
            {"label": "E", "option_text": "Not measured", "weight": 5},
        ],
    },
    {
        "question_code": "SWE4_L1_05",
        "process": "SWE.4",
        "level": "L1",
        "criteria": "SWE.4.BP4 — Bidirectional traceability between units, criteria, results",
        "identifies": "Test-result orphaning",
        "stakeholders": ["TE", "QA", "ASR"],
        "question_text": "How are unit-test results linked to verification criteria and units?",
        "recommendation_logic": "Recommend test-management tool integration (e.g., qTest/Jama/Polarion).",
        "options": [
            {"label": "A", "option_text": "Tool-enforced bidirectional links; audited each release", "weight": 0},
            {"label": "B", "option_text": "Manual matrix maintained", "weight": 2},
            {"label": "C", "option_text": "Links exist for failed tests only", "weight": 3},
            {"label": "D", "option_text": "Linked only when assessor asks", "weight": 4},
            {"label": "E", "option_text": "Not linked", "weight": 5},
        ],
    },
    {
        "question_code": "SWE4_L2_06",
        "process": "SWE.4",
        "level": "L2",
        "criteria": "GP 2.1.6, GP 2.1.7 — Resources & stakeholder management for SWE.4",
        "identifies": "Under-resourced verification, late access to HW/test bench",
        "stakeholders": ["PM", "TL", "TE"],
        "question_text": "How is access to test infrastructure (HIL/SIL, test benches, target boards) planned and assured for unit verification?",
        "recommendation_logic": "Strongest \"release-phase\" predictor; recommend resource calendar + escalation.",
        "options": [
            {"label": "A", "option_text": "Infrastructure capacity planned per release; bottleneck escalation defined", "weight": 0},
            {"label": "B", "option_text": "Plan exists but no escalation path", "weight": 2},
            {"label": "C", "option_text": "Access requested per sprint", "weight": 3},
            {"label": "D", "option_text": "Access negotiated when needed", "weight": 4},
            {"label": "E", "option_text": "Frequent blocking due to unavailable HW", "weight": 5},
        ],
    },
    {
        "question_code": "SWE4_L2_07",
        "process": "SWE.4",
        "level": "L2",
        "criteria": "GP 2.2.3, GP 2.2.4 — Work-product control & review of unit-verification reports",
        "identifies": "Reports not under configuration control",
        "stakeholders": ["QA"],
        "question_text": "How are unit-verification reports stored, versioned, and reviewed?",
        "recommendation_logic": "Recommend CM-controlled report storage (referenced SUP.8).",
        "options": [
            {"label": "A", "option_text": "Versioned in CM with status workflow + reviewer sign-off", "weight": 0},
            {"label": "B", "option_text": "Versioned only", "weight": 2},
            {"label": "C", "option_text": "Stored on shared drive, no versioning", "weight": 3},
            {"label": "D", "option_text": "Stored locally", "weight": 4},
            {"label": "E", "option_text": "Not formally stored", "weight": 5},
        ],
    },
    # -----------------------------------------------------------------------
    # SWE.5 — Software Component Verification and Integration Verification
    # -----------------------------------------------------------------------
    {
        "question_code": "SWE5_L1_01",
        "process": "SWE.5",
        "level": "L1",
        "criteria": "SWE.5.BP1 — Specify integration-verification measures",
        "identifies": "Missing integration-verification scope",
        "stakeholders": ["TE", "SA"],
        "question_text": "How are integration-verification measures defined for the integrated software?",
        "recommendation_logic": "Recommend interface-driven integration-verification specs.",
        "options": [
            {"label": "A", "option_text": "Per-component and per-interface measures derived from architecture", "weight": 0},
            {"label": "B", "option_text": "Per-component only", "weight": 2},
            {"label": "C", "option_text": "End-to-end tests only", "weight": 3},
            {"label": "D", "option_text": "Defined as needed", "weight": 4},
            {"label": "E", "option_text": "Not defined", "weight": 5},
        ],
    },
    {
        "question_code": "SWE5_L1_02",
        "process": "SWE.5",
        "level": "L1",
        "criteria": "SWE.5.BP2 — Specify component-behaviour verification measures (PAM 4.0 novelty)",
        "identifies": "Component-level black-box gaps",
        "stakeholders": ["TE", "SA"],
        "question_text": "How is software-component behaviour verified before integration?",
        "recommendation_logic": "New PAM 4.0 expectation; high signal of legacy 3.1 process.",
        "options": [
            {"label": "A", "option_text": "Component contract tests run against published interfaces in CI", "weight": 0},
            {"label": "B", "option_text": "Component tests exist but run manually", "weight": 2},
            {"label": "C", "option_text": "Verified only as part of integration", "weight": 3},
            {"label": "D", "option_text": "Verified only at qualification", "weight": 4},
            {"label": "E", "option_text": "Not verified at component level", "weight": 5},
        ],
    },
    {
        "question_code": "SWE5_L1_03",
        "process": "SWE.5",
        "level": "L1",
        "criteria": "SWE.5.BP3 — Select verification measures incl. regression",
        "identifies": "Selection criteria absent",
        "stakeholders": ["TE"],
        "question_text": "How are integration-test cases selected per release (including regression)?",
        "recommendation_logic": "Recommend traceable selection rules linked to release scope.",
        "options": [
            {"label": "A", "option_text": "Selection rules + change-impact-driven regression set documented", "weight": 0},
            {"label": "B", "option_text": "Regression rules only", "weight": 2},
            {"label": "C", "option_text": "\"Run everything\"", "weight": 2},
            {"label": "D", "option_text": "Selected ad-hoc", "weight": 4},
            {"label": "E", "option_text": "No selection criteria", "weight": 5},
        ],
    },
    {
        "question_code": "SWE5_L1_04",
        "process": "SWE.5",
        "level": "L1",
        "criteria": "SWE.5.BP4 — Integrate elements & perform integration verification",
        "identifies": "Big-bang integration risk",
        "stakeholders": ["SD", "TE", "SA"],
        "question_text": "How are software elements integrated and verified?",
        "recommendation_logic": "High signal of late defects; recommend stepwise integration plan with CI.",
        "options": [
            {"label": "A", "option_text": "Continuous integration with stepwise integration plan and per-step verification", "weight": 0},
            {"label": "B", "option_text": "Stepwise integration but verification batched", "weight": 2},
            {"label": "C", "option_text": "Daily integration without integration plan", "weight": 3},
            {"label": "D", "option_text": "Big-bang integration at end of sprint", "weight": 4},
            {"label": "E", "option_text": "Big-bang integration at end of release", "weight": 5},
        ],
    },
    {
        "question_code": "SWE5_L1_05",
        "process": "SWE.5",
        "level": "L1",
        "criteria": "SWE.5.BP5 — Perform component verification & record",
        "identifies": "Result records missing",
        "stakeholders": ["QA", "TE"],
        "question_text": "How are component-verification and integration-verification results recorded?",
        "recommendation_logic": "Recommend tool-based recording with environment fingerprint.",
        "options": [
            {"label": "A", "option_text": "Recorded automatically in test-management tool with status, evidence, environment metadata", "weight": 0},
            {"label": "B", "option_text": "Recorded in test tool, no environment metadata", "weight": 2},
            {"label": "C", "option_text": "Captured in spreadsheets", "weight": 3},
            {"label": "D", "option_text": "Captured in e-mail/chat", "weight": 4},
            {"label": "E", "option_text": "Not recorded", "weight": 5},
        ],
    },
    {
        "question_code": "SWE5_L1_06",
        "process": "SWE.5",
        "level": "L1",
        "criteria": "SWE.5.BP6 — Consistency & bidirectional traceability (arch / detailed design ↔ verification measures ↔ results)",
        "identifies": "Verification-result orphaning at integration",
        "stakeholders": ["QA", "ASR"],
        "question_text": "What is the state of bidirectional traceability between architecture/design, integration verification measures, and results?",
        "recommendation_logic": "Compose with SWE2_L1_05 for compounded signal.",
        "options": [
            {"label": "A", "option_text": "Tool-enforced bidirectional links with periodic audits", "weight": 0},
            {"label": "B", "option_text": "Forward only", "weight": 2},
            {"label": "C", "option_text": "Spreadsheet matrix", "weight": 3},
            {"label": "D", "option_text": "Implicit", "weight": 4},
            {"label": "E", "option_text": "None", "weight": 5},
        ],
    },
    {
        "question_code": "SWE5_L2_07",
        "process": "SWE.5",
        "level": "L2",
        "criteria": "GP 2.1.4 — Adjust process performance (interface management between SD & integration team)",
        "identifies": "Interface miscommunication between teams",
        "stakeholders": ["TL", "PM"],
        "question_text": "How are interface changes coordinated between development and integration teams?",
        "recommendation_logic": "PA 2.1 / GP 2.1.7 (involved-party management); recommend lightweight ICB.",
        "options": [
            {"label": "A", "option_text": "Interface change board with affected-party notification SLA", "weight": 0},
            {"label": "B", "option_text": "E-mail notification policy in place", "weight": 2},
            {"label": "C", "option_text": "Notified during integration only", "weight": 3},
            {"label": "D", "option_text": "Discovered during failure", "weight": 4},
            {"label": "E", "option_text": "No coordination mechanism", "weight": 5},
        ],
    },
    # -----------------------------------------------------------------------
    # SWE.6 — Software Verification (formerly Software Qualification Test)
    # -----------------------------------------------------------------------
    {
        "question_code": "SWE6_L1_01",
        "process": "SWE.6",
        "level": "L1",
        "criteria": "SWE.6.BP1 — Specify verification measures vs. SW requirements",
        "identifies": "Test cases not derived from SW requirements",
        "stakeholders": ["TE"],
        "question_text": "How are software-verification measures derived from SW requirements?",
        "recommendation_logic": "Recommend req-to-test allocation report at each baseline.",
        "options": [
            {"label": "A", "option_text": "Each SW requirement has at least one verification measure recorded with technique justification", "weight": 0},
            {"label": "B", "option_text": "Coverage exists but technique not justified", "weight": 2},
            {"label": "C", "option_text": "Coverage is partial", "weight": 3},
            {"label": "D", "option_text": "Tests written from intuition", "weight": 4},
            {"label": "E", "option_text": "Not derived from SW requirements", "weight": 5},
        ],
    },
    {
        "question_code": "SWE6_L1_02",
        "process": "SWE.6",
        "level": "L1",
        "criteria": "SWE.6.BP2 — Select verification measures incl. regression (release scope)",
        "identifies": "Regression policy weak at qualification",
        "stakeholders": ["TE", "PM"],
        "question_text": "How are SWE.6 verification measures selected for the release, including regression?",
        "recommendation_logic": "High signal pre-release; flag if release phase = late.",
        "options": [
            {"label": "A", "option_text": "Documented selection per release with risk-based regression set", "weight": 0},
            {"label": "B", "option_text": "Selection per release without risk weighting", "weight": 2},
            {"label": "C", "option_text": "Always full re-run", "weight": 2},
            {"label": "D", "option_text": "Selected verbally per stand-up", "weight": 4},
            {"label": "E", "option_text": "No selection process", "weight": 5},
        ],
    },
    {
        "question_code": "SWE6_L1_03",
        "process": "SWE.6",
        "level": "L1",
        "criteria": "SWE.6.BP3 — Verify integrated SW & record (qualification environment)",
        "identifies": "Wrong target / non-representative env.",
        "stakeholders": ["TE", "QA"],
        "question_text": "What environment is used for SWE.6 qualification verification?",
        "recommendation_logic": "Recommend escalation to HIL for safety-critical functions.",
        "options": [
            {"label": "A", "option_text": "Representative target HW (HIL/real ECU) with calibrated parameters", "weight": 0},
            {"label": "B", "option_text": "HIL only", "weight": 2},
            {"label": "C", "option_text": "SIL/MIL with HW abstraction", "weight": 3},
            {"label": "D", "option_text": "PC simulation", "weight": 4},
            {"label": "E", "option_text": "Developer machine", "weight": 5},
        ],
    },
    {
        "question_code": "SWE6_L1_04",
        "process": "SWE.6",
        "level": "L1",
        "criteria": "SWE.6.BP4 — Consistency & bidirectional traceability (SW reqs ↔ test specs ↔ results)",
        "identifies": "Final-stage traceability gap",
        "stakeholders": ["QA", "ASR"],
        "question_text": "How is bidirectional traceability maintained between SW requirements, qualification test specs, and results?",
        "recommendation_logic": "Compose with SWE1_L1_05; if both high → critical traceability red flag.",
        "options": [
            {"label": "A", "option_text": "Tool-enforced and audited each release", "weight": 0},
            {"label": "B", "option_text": "Maintained but not audited", "weight": 2},
            {"label": "C", "option_text": "Spreadsheet", "weight": 3},
            {"label": "D", "option_text": "Manual when needed", "weight": 4},
            {"label": "E", "option_text": "None", "weight": 5},
        ],
    },
    {
        "question_code": "SWE6_L1_05",
        "process": "SWE.6",
        "level": "L1",
        "criteria": "SWE.6.BP5 — Summarise & communicate results",
        "identifies": "Defect leakage / no test summary",
        "stakeholders": ["QA", "PM"],
        "question_text": "How are qualification-test results summarised and communicated to affected parties?",
        "recommendation_logic": "Recommend templated test summary tied to release approval.",
        "options": [
            {"label": "A", "option_text": "Versioned test-summary report per release with go/no-go criteria", "weight": 0},
            {"label": "B", "option_text": "Report exists but no go/no-go criteria", "weight": 2},
            {"label": "C", "option_text": "Slide summary at release meeting", "weight": 3},
            {"label": "D", "option_text": "Verbal summary", "weight": 4},
            {"label": "E", "option_text": "Not communicated", "weight": 5},
        ],
    },
    {
        "question_code": "SWE6_L2_06",
        "process": "SWE.6",
        "level": "L2",
        "criteria": "GP 2.2.2 — Work-product requirements (defect management)",
        "identifies": "Defect process weak at qualification",
        "stakeholders": ["QA", "TE"],
        "question_text": "How are qualification-test defects managed and triaged?",
        "recommendation_logic": "Reference SUP.9 (out of scope); recommend root-cause field.",
        "options": [
            {"label": "A", "option_text": "Defects in tracker with severity, owner, SLA, root-cause field; weekly triage", "weight": 0},
            {"label": "B", "option_text": "Tracker used; no triage cadence", "weight": 2},
            {"label": "C", "option_text": "Defects in spreadsheet", "weight": 3},
            {"label": "D", "option_text": "Verbally tracked", "weight": 4},
            {"label": "E", "option_text": "No defect tracking", "weight": 5},
        ],
    },
    {
        "question_code": "SWE6_L3_07",
        "process": "SWE.6",
        "level": "L3",
        "criteria": "GP 3.2.4 — Monitor performance of defined process (information, not data)",
        "identifies": "No process-improvement feedback loop",
        "stakeholders": ["ASR", "QA", "PM"],
        "question_text": "How is information from SWE.6 fed back into the organisational standard process?",
        "recommendation_logic": "PA 3.2 weakness; recommend a quarterly Process Group review channel.",
        "options": [
            {"label": "A", "option_text": "Lessons-learned + KPIs reported to Process Group; standard process updated", "weight": 0},
            {"label": "B", "option_text": "Lessons-learned written, no link to standard process", "weight": 2},
            {"label": "C", "option_text": "Discussed in retro only", "weight": 3},
            {"label": "D", "option_text": "Captured in private notes", "weight": 4},
            {"label": "E", "option_text": "No feedback loop", "weight": 5},
        ],
    },
]


def seed():
    inserted_q = 0
    inserted_o = 0
    skipped = 0

    with Session(engine) as session:
        for q_data in QUESTIONS:
            # Idempotent: skip if already seeded
            existing = session.exec(
                select(AuditQuestion).where(AuditQuestion.question_code == q_data["question_code"])
            ).first()
            if existing:
                skipped += 1
                continue

            question = AuditQuestion(
                question_code=q_data["question_code"],
                base_practice_id=extract_base_practice_id(q_data["criteria"]),
                process=PROCESS_MAP[q_data["process"]],
                level=q_data["level"],
                stakeholders=[STAKEHOLDER_MAP[s] for s in q_data["stakeholders"]],
                question_text=q_data["question_text"],
                recommendation_logic=q_data["recommendation_logic"],
                created_at=datetime.now(timezone.utc),
            )
            session.add(question)
            session.flush()  # get auto-assigned question.id before inserting options

            for opt in q_data["options"]:
                option = AuditOption(
                    question_id=question.id,
                    label=opt["label"],
                    option_text=opt["option_text"],
                    weight=min(opt["weight"], 4),  # clamp legacy weight=5 to 4
                )
                session.add(option)
                inserted_o += 1

            inserted_q += 1

        session.commit()

    print(f"Done. Inserted {inserted_q} questions, {inserted_o} options. Skipped {skipped} (already existed).")


if __name__ == "__main__":
    seed()
