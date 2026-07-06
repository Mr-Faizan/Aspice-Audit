"""
LinUCB Contextual Multi-Armed Bandit engine for adaptive ASPICE audit question selection.

Context vector (23 dims):
  [0:7]   one-hot stakeholder role  (7 dims)
  [7]     session progress           (1 dim)
  [8:14]  per-process coverage flag  (6 dims, SWE1-SWE6)
  [14:17] per-level coverage flag    (3 dims, L1-L3)
  [17:23] running mean weakness score per process (6 dims)
"""
from datetime import datetime, timezone

import numpy as np
from sqlmodel import Session, select

from app.models import (
    AspiceLevelEnum,
    AuditOption,
    AuditQuestion,
    AuditResponse,
    AuditSession,
    BanditArmState,
    ProcessEnum,
    StakeholderRoleEnum,
    User,
)

_ALPHA = 1.0  # UCB exploration coefficient
_CONTEXT_DIM = 23

_ROLES = list(StakeholderRoleEnum)   # fixed order for one-hot encoding
_PROCESSES = list(ProcessEnum)       # SWE1 … SWE6
_LEVELS = list(AspiceLevelEnum)      # L1, L2, L3


# ---------------------------------------------------------------------------
# 3.2.1 — build_context
# ---------------------------------------------------------------------------

def build_context(session: AuditSession, user: User, db: Session) -> np.ndarray:
    """Return a 23-dim feature vector describing the current audit state."""
    ctx = np.zeros(_CONTEXT_DIM, dtype=float)

    # [0:7] one-hot stakeholder role
    ctx[_ROLES.index(user.stakeholder_role)] = 1.0

    # [7] session progress
    ctx[7] = len(session.questions_asked) / session.max_questions

    if session.questions_asked:
        questions = db.exec(
            select(AuditQuestion).where(AuditQuestion.id.in_(session.questions_asked))
        ).all()

        asked_processes = {q.process for q in questions}
        asked_levels = {q.level for q in questions}

        # [8:14] per-process coverage flags
        for i, p in enumerate(_PROCESSES):
            ctx[8 + i] = 1.0 if p in asked_processes else 0.0

        # [14:17] per-level coverage flags
        for i, lv in enumerate(_LEVELS):
            ctx[14 + i] = 1.0 if lv in asked_levels else 0.0

        # [17:23] running mean weakness score per process
        rows = db.exec(
            select(AuditResponse, AuditOption)
            .join(AuditOption, AuditOption.id == AuditResponse.option_id)
            .where(AuditResponse.session_id == session.id)
        ).all()

        q_by_id = {q.id: q for q in questions}
        process_weights: dict[ProcessEnum, list[float]] = {p: [] for p in _PROCESSES}
        for response, option in rows:
            q = q_by_id.get(response.question_id)
            if q:
                process_weights[q.process].append(option.weight / 4.0)

        for i, p in enumerate(_PROCESSES):
            ws = process_weights[p]
            ctx[17 + i] = sum(ws) / len(ws) if ws else 0.0

    return ctx


# ---------------------------------------------------------------------------
# 3.2.2 — select_question
# ---------------------------------------------------------------------------

def select_question(
    context: np.ndarray,
    eligible_questions: list[AuditQuestion],
    db: Session,
) -> AuditQuestion:
    """Return the question with the highest LinUCB score."""
    best_question = eligible_questions[0]
    best_score = -float("inf")

    for question in eligible_questions:
        A, b = _load_or_init_arm(question.id, db)
        A_inv = np.linalg.inv(A)
        theta = A_inv @ b
        score = float(theta @ context + _ALPHA * np.sqrt(context @ A_inv @ context))

        if score > best_score:
            best_score = score
            best_question = question

    return best_question


# ---------------------------------------------------------------------------
# 3.2.3 — compute_reward
# ---------------------------------------------------------------------------

def compute_reward(
    option: AuditOption,
    question: AuditQuestion,
    session: AuditSession,
    db: Session,
) -> float:
    """Base reward = weight / 4.0; +0.2 coverage bonus if process is new in session."""
    reward = option.weight / 4.0

    if not session.questions_asked:
        # No questions asked yet — any process is new
        reward += 0.2
    else:
        asked_qs = db.exec(
            select(AuditQuestion).where(AuditQuestion.id.in_(session.questions_asked))
        ).all()
        covered_processes = {q.process for q in asked_qs}
        if question.process not in covered_processes:
            reward += 0.2

    return min(1.0, reward)


# ---------------------------------------------------------------------------
# 3.2.4 — update_arm
# ---------------------------------------------------------------------------

def update_arm(
    question_id: int,
    context: np.ndarray,
    reward: float,
    db: Session,
) -> None:
    """LinUCB update: A = A + x·xᵀ, b = b + reward·x. Persist to DB."""
    arm = db.exec(
        select(BanditArmState).where(BanditArmState.question_id == question_id)
    ).first()

    if arm is None:
        arm = BanditArmState(
            question_id=question_id,
            A_matrix=np.eye(_CONTEXT_DIM).tolist(),
            b_vector=np.zeros(_CONTEXT_DIM).tolist(),
            pull_count=0,
            total_reward=0.0,
            updated_at=datetime.now(timezone.utc),
        )
        db.add(arm)
        db.flush()

    A = np.array(arm.A_matrix)
    b = np.array(arm.b_vector)

    A += np.outer(context, context)
    b += reward * context

    arm.A_matrix = A.tolist()
    arm.b_vector = b.tolist()
    arm.pull_count += 1
    arm.total_reward += reward
    arm.updated_at = datetime.now(timezone.utc)

    db.add(arm)
    db.commit()


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

def _load_or_init_arm(question_id: int, db: Session) -> tuple[np.ndarray, np.ndarray]:
    """Load BanditArmState or return identity A, zero b if first encounter."""
    arm = db.exec(
        select(BanditArmState).where(BanditArmState.question_id == question_id)
    ).first()

    if arm is None or not arm.A_matrix:
        return np.eye(_CONTEXT_DIM), np.zeros(_CONTEXT_DIM)

    return np.array(arm.A_matrix), np.array(arm.b_vector)
