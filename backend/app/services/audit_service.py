"""
Audit Service — orchestrates the full audit session lifecycle.

Connects the CMAB engine (question selection + learning) with the
weakness classifier (scoring + gap identification).
"""
import uuid
from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel
from sqlmodel import Session, select

from app.models import (
    AuditOption,
    AuditQuestion,
    AuditQuestionPublic,
    AuditOptionPublic,
    AuditResponse,
    AuditSession,
    SessionStatusEnum,
    User,
    WeaknessResult,
)
from app.services import cmab_engine, weakness_classifier


# ---------------------------------------------------------------------------
# Response schema returned by submit_answer
# ---------------------------------------------------------------------------

class AnswerResultInProgress(BaseModel):
    status: Literal["in_progress"]
    next_question: AuditQuestionPublic
    questions_answered: int
    questions_total: int


class AnswerResultCompleted(BaseModel):
    status: Literal["completed"]
    session_id: uuid.UUID
    top_weaknesses: list[str]


# Union type the API route returns
AnswerResult = AnswerResultInProgress | AnswerResultCompleted


# ---------------------------------------------------------------------------
# 5.1.1 — start_session
# ---------------------------------------------------------------------------

def start_session(user: User, db: Session) -> tuple[AuditSession, AuditQuestionPublic]:
    """
    Create a new AuditSession, select the first question via CMAB, and
    return both the session and the question (with its options) ready to display.
    """
    session = AuditSession(
        user_id=user.id,
        status=SessionStatusEnum.in_progress,
        questions_asked=[],
        started_at=datetime.now(timezone.utc),
    )
    db.add(session)
    db.flush()  # get session.id before the next queries

    context = cmab_engine.build_context(session, user, db)
    eligible = _get_eligible_questions(session, db)

    if not eligible:
        raise ValueError("No eligible questions available to start a session.")

    first_question = cmab_engine.select_question(context, eligible, db)

    session.questions_asked = [first_question.id]
    db.add(session)
    db.commit()
    db.refresh(session)

    return session, _to_public(first_question, db)


# ---------------------------------------------------------------------------
# 5.1.2 — submit_answer
# ---------------------------------------------------------------------------

def submit_answer(
    session_id: uuid.UUID,
    question_id: int,
    option_id: int,
    db: Session,
) -> AnswerResult:
    """
    Record the user's answer, update the CMAB arm, then either return the
    next question (in_progress) or complete the session and return results.

    Raises ValueError on invalid session state or mismatched question.
    """
    session = db.get(AuditSession, session_id)
    if session is None:
        raise ValueError(f"Session {session_id} not found.")
    if session.status != SessionStatusEnum.in_progress:
        raise ValueError(f"Session {session_id} is already {session.status.value}.")

    # Guard: the submitted question must be the last one we sent the user
    if not session.questions_asked or session.questions_asked[-1] != question_id:
        raise ValueError(
            f"question_id {question_id} does not match the current question "
            f"(expected {session.questions_asked[-1] if session.questions_asked else 'none'})."
        )

    # Validate option belongs to the question
    option = db.get(AuditOption, option_id)
    if option is None or option.question_id != question_id:
        raise ValueError(f"option_id {option_id} is not valid for question {question_id}.")

    question = db.get(AuditQuestion, question_id)

    # Record the response
    response = AuditResponse(
        session_id=session_id,
        question_id=question_id,
        option_id=option_id,
    )
    db.add(response)
    db.flush()

    # CMAB update
    context = cmab_engine.build_context(session, session.user, db)
    reward = cmab_engine.compute_reward(option, question, session, db)
    cmab_engine.update_arm(question_id, context, reward, db)

    questions_answered = len(session.questions_asked)

    # Decide: continue or complete?
    eligible = _get_eligible_questions(session, db)
    budget_exhausted = questions_answered >= session.max_questions

    if budget_exhausted or not eligible:
        weakness_result = _complete_session(session, db)
        return AnswerResultCompleted(
            status="completed",
            session_id=session.id,
            top_weaknesses=weakness_result.top_weaknesses,
        )

    # Select next question
    updated_context = cmab_engine.build_context(session, session.user, db)
    next_question = cmab_engine.select_question(updated_context, eligible, db)
    session.questions_asked = session.questions_asked + [next_question.id]
    db.add(session)
    db.commit()
    db.refresh(session)

    return AnswerResultInProgress(
        status="in_progress",
        next_question=_to_public(next_question, db),
        questions_answered=len(session.questions_asked) - 1,
        questions_total=session.max_questions,
    )


# ---------------------------------------------------------------------------
# 5.1.3 — complete_session (internal, also callable directly)
# ---------------------------------------------------------------------------

def _complete_session(session: AuditSession, db: Session) -> WeaknessResult:
    """
    Compute weakness scores, persist WeaknessResult, mark session completed.
    """
    scores = weakness_classifier.compute_scores(session.id, db)
    top_weaknesses = weakness_classifier.get_top_weaknesses(scores, n=3)

    result = WeaknessResult(
        session_id=session.id,
        scores=scores,
        top_weaknesses=top_weaknesses,
        computed_at=datetime.now(timezone.utc),
    )
    db.add(result)

    session.status = SessionStatusEnum.completed
    session.completed_at = datetime.now(timezone.utc)
    db.add(session)

    db.commit()
    db.refresh(result)
    return result


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_eligible_questions(session: AuditSession, db: Session) -> list[AuditQuestion]:
    """Active questions not yet asked in this session."""
    asked_ids = session.questions_asked or []
    query = select(AuditQuestion).where(AuditQuestion.is_active == True)  # noqa: E712
    if asked_ids:
        query = query.where(AuditQuestion.id.not_in(asked_ids))
    return list(db.exec(query).all())


def _to_public(question: AuditQuestion, db: Session) -> AuditQuestionPublic:
    """Load options and build the public schema for a question."""
    options = db.exec(
        select(AuditOption).where(AuditOption.question_id == question.id)
    ).all()
    return AuditQuestionPublic(
        id=question.id,
        question_code=question.question_code,
        base_practice_id=question.base_practice_id,
        process=question.process,
        level=question.level,
        stakeholders=question.stakeholders,
        question_text=question.question_text,
        recommendation_logic=question.recommendation_logic,
        is_active=question.is_active,
        options=[
            AuditOptionPublic(
                id=o.id,
                label=o.label,
                option_text=o.option_text,
                weight=o.weight,
            )
            for o in sorted(options, key=lambda o: o.label)
        ],
    )
