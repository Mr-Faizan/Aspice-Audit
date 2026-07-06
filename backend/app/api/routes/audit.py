"""
Audit session routes.

POST  /audit/sessions/          — start a new session (any authenticated user)
GET   /audit/sessions/          — list the current user's sessions
GET   /audit/sessions/{id}      — get one session (own or admin)
POST  /audit/sessions/{id}/answer — submit an answer
GET   /audit/sessions/{id}/results — get weakness results
"""
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import col, select

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.models import (
    AuditSession,
    AuditQuestionPublic,
    AuditSessionPublic,
    SessionStatusEnum,
    WeaknessResultPublic,
)
from app.services import audit_service
from app.services.audit_service import AnswerResult

router = APIRouter()


# ---------------------------------------------------------------------------
# Request / combined-response schemas
# ---------------------------------------------------------------------------

class SessionStart(BaseModel):
    """Response for POST /audit/sessions/ — session metadata + first question."""
    session: AuditSessionPublic
    first_question: AuditQuestionPublic


class AnswerIn(BaseModel):
    question_id: int
    option_id: int


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_session_or_404(session_id: uuid.UUID, db: SessionDep) -> AuditSession:
    audit_session = db.get(AuditSession, session_id)
    if not audit_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return audit_session


def _assert_owns_session(audit_session: AuditSession, current_user: Any) -> None:
    if audit_session.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorised to access this session")


# ---------------------------------------------------------------------------
# 6.1.1 — POST /audit/sessions/
# ---------------------------------------------------------------------------

@router.post("/", response_model=SessionStart, status_code=201)
def start_session(
    db: SessionDep,
    current_user: CurrentUser,
) -> Any:
    """Start a new audit session for the authenticated user."""
    try:
        audit_session, first_question = audit_service.start_session(current_user, db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return SessionStart(
        session=AuditSessionPublic.model_validate(audit_session),
        first_question=first_question,
    )


# ---------------------------------------------------------------------------
# 6.1.2 — GET /audit/sessions/
# ---------------------------------------------------------------------------

@router.get("/", response_model=list[AuditSessionPublic])
def list_sessions(
    db: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 20,
) -> Any:
    """List the authenticated user's sessions, newest first."""
    sessions = db.exec(
        select(AuditSession)
        .where(AuditSession.user_id == current_user.id)
        .order_by(col(AuditSession.started_at).desc())
        .offset(skip)
        .limit(limit)
    ).all()
    return sessions


# ---------------------------------------------------------------------------
# 6.1.3 — GET /audit/sessions/{id}
# ---------------------------------------------------------------------------

@router.get("/{session_id}", response_model=AuditSessionPublic)
def get_session(
    session_id: uuid.UUID,
    db: SessionDep,
    current_user: CurrentUser,
) -> Any:
    """Retrieve a single session by ID (own session or admin)."""
    audit_session = _get_session_or_404(session_id, db)
    _assert_owns_session(audit_session, current_user)
    return audit_session


# ---------------------------------------------------------------------------
# 6.1.4 — POST /audit/sessions/{id}/answer
# ---------------------------------------------------------------------------

@router.post("/{session_id}/answer", response_model=AnswerResult)
def submit_answer(
    session_id: uuid.UUID,
    answer: AnswerIn,
    db: SessionDep,
    current_user: CurrentUser,
) -> Any:
    """
    Submit an answer for the current question.

    Returns either:
    - `{ status: "in_progress", next_question, questions_answered, questions_total }`
    - `{ status: "completed", session_id, top_weaknesses }`
    """
    audit_session = _get_session_or_404(session_id, db)
    _assert_owns_session(audit_session, current_user)

    try:
        result = audit_service.submit_answer(
            session_id=session_id,
            question_id=answer.question_id,
            option_id=answer.option_id,
            db=db,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return result


# ---------------------------------------------------------------------------
# 6.1.5 — GET /audit/sessions/{id}/results
# ---------------------------------------------------------------------------

@router.get("/{session_id}/results", response_model=WeaknessResultPublic)
def get_results(
    session_id: uuid.UUID,
    db: SessionDep,
    current_user: CurrentUser,
) -> Any:
    """Get weakness results for a completed session."""
    audit_session = _get_session_or_404(session_id, db)
    _assert_owns_session(audit_session, current_user)

    if audit_session.status != SessionStatusEnum.completed:
        raise HTTPException(
            status_code=400,
            detail="Session is not completed yet — answer all questions first",
        )

    weakness_result = audit_session.weakness_result
    if not weakness_result:
        raise HTTPException(status_code=404, detail="Results not found for this session")

    return weakness_result
