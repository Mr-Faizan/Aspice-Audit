"""
Weakness Classifier — computes per-(process, level) risk scores from a completed
AuditSession and identifies the most critical gaps.

Score scale: 0.0 = fully compliant, 1.0 = critical gap.
"""
import uuid

from sqlmodel import Session, select

from app.models import (
    AspiceLevelEnum,
    AuditOption,
    AuditQuestion,
    AuditResponse,
    ProcessEnum,
)

_PROCESSES = list(ProcessEnum)   # SWE1 … SWE6
_LEVELS = list(AspiceLevelEnum)  # L1, L2, L3


# ---------------------------------------------------------------------------
# 4.1.1 — compute_scores
# ---------------------------------------------------------------------------

def compute_scores(session_id: uuid.UUID, db: Session) -> dict:
    """
    For every (process, level) pair compute a normalised risk score.

    Returns a nested dict:
        {
          "SWE1": {"L1": 0.75, "L2": null, "L3": null},
          "SWE2": {"L1": 0.25, "L2": 0.5,  "L3": null},
          ...
        }
    A null score means no question for that pair was answered in this session.
    """
    # Fetch all responses for the session, joining to get option weight and
    # question process/level in one query.
    rows = db.exec(
        select(AuditResponse, AuditOption, AuditQuestion)
        .join(AuditOption, AuditOption.id == AuditResponse.option_id)
        .join(AuditQuestion, AuditQuestion.id == AuditResponse.question_id)
        .where(AuditResponse.session_id == session_id)
    ).all()

    # Bucket weights by (process, level)
    buckets: dict[tuple[ProcessEnum, AspiceLevelEnum], list[float]] = {}
    for _response, option, question in rows:
        key = (question.process, question.level)
        buckets.setdefault(key, []).append(option.weight / 4.0)

    # Build the nested result dict
    scores: dict[str, dict[str, float | None]] = {}
    for process in _PROCESSES:
        scores[process.value] = {}
        for level in _LEVELS:
            weights = buckets.get((process, level))
            if weights:
                scores[process.value][level.value] = sum(weights) / len(weights)
            else:
                scores[process.value][level.value] = None

    return scores


# ---------------------------------------------------------------------------
# 4.1.2 — classify
# ---------------------------------------------------------------------------

def classify(score: float | None) -> str:
    """Map a normalised score to a human-readable risk category."""
    if score is None:
        return "not_assessed"
    if score <= 0.25:
        return "compliant"
    if score <= 0.50:
        return "minor_weakness"
    if score <= 0.75:
        return "significant_gap"
    return "critical_gap"


# ---------------------------------------------------------------------------
# 4.1.3 — get_top_weaknesses
# ---------------------------------------------------------------------------

def get_top_weaknesses(scores: dict, n: int = 3) -> list[str]:
    """
    Return the top-n (process, level) keys with the highest risk scores.

    Keys are formatted as "SWE1-L1", "SWE3-L2", etc.
    Null (not-assessed) pairs are excluded.
    """
    pairs: list[tuple[str, float]] = []

    for process_key, levels in scores.items():
        for level_key, score in levels.items():
            if score is not None:
                pairs.append((f"{process_key}-{level_key}", score))

    pairs.sort(key=lambda p: p[1], reverse=True)
    return [key for key, _ in pairs[:n]]
