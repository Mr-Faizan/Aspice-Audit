"""
Question bank admin routes (all endpoints require superuser).

GET    /questions/       — list with filters
POST   /questions/       — create question + options
PATCH  /questions/{id}   — update question or options
DELETE /questions/{id}   — soft delete (is_active = False)
POST   /questions/seed   — bulk idempotent seed
"""
import uuid
from typing import Annotated, Any

import numpy as np
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import col, select

from app.api.deps import SessionDep, get_current_active_superuser
from app.models import (
    AspiceLevelEnum,
    AuditOption,
    AuditOptionPublic,
    AuditQuestion,
    AuditQuestionPublic,
    BanditArmState,
    Message,
    ProcessEnum,
    StakeholderRoleEnum,
)

_CONTEXT_DIM = 23
SuperuserDep = Annotated[Any, Depends(get_current_active_superuser)]

router = APIRouter()


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------

class OptionIn(BaseModel):
    label: str = Field(max_length=5)
    option_text: str = Field(max_length=1000)
    weight: int = Field(ge=0, le=4)


class QuestionIn(BaseModel):
    question_code: str = Field(max_length=50)
    base_practice_id: str = Field(max_length=50)
    process: ProcessEnum
    level: AspiceLevelEnum
    stakeholders: list[StakeholderRoleEnum] = []
    question_text: str = Field(max_length=2048)
    recommendation_logic: str | None = None
    options: list[OptionIn] = Field(min_length=1)


class QuestionUpdate(BaseModel):
    base_practice_id: str | None = None
    process: ProcessEnum | None = None
    level: AspiceLevelEnum | None = None
    stakeholders: list[StakeholderRoleEnum] | None = None
    question_text: str | None = None
    recommendation_logic: str | None = None
    is_active: bool | None = None
    options: list[OptionIn] | None = None  # if provided, replaces all options


class SeedIn(BaseModel):
    questions: list[QuestionIn]


class SeedResult(BaseModel):
    inserted: int
    skipped: int


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_question_or_404(question_id: int, db: SessionDep) -> AuditQuestion:
    q = db.get(AuditQuestion, question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q


def _to_public(q: AuditQuestion, db: SessionDep) -> AuditQuestionPublic:
    options = db.exec(
        select(AuditOption).where(AuditOption.question_id == q.id)
    ).all()
    return AuditQuestionPublic(
        id=q.id,
        question_code=q.question_code,
        base_practice_id=q.base_practice_id,
        process=q.process,
        level=q.level,
        stakeholders=q.stakeholders,
        question_text=q.question_text,
        recommendation_logic=q.recommendation_logic,
        is_active=q.is_active,
        options=[
            AuditOptionPublic(id=o.id, label=o.label, option_text=o.option_text, weight=o.weight)
            for o in sorted(options, key=lambda o: o.label)
        ],
    )


def _init_bandit_arm(question_id: int, db: SessionDep) -> None:
    """Create a fresh BanditArmState (identity A, zero b) for a new question."""
    A = np.eye(_CONTEXT_DIM).tolist()
    b = np.zeros(_CONTEXT_DIM).tolist()
    arm = BanditArmState(
        question_id=question_id,
        A_matrix=A,
        b_vector=b,
    )
    db.add(arm)


def _replace_options(question_id: int, options_in: list[OptionIn], db: SessionDep) -> None:
    existing = db.exec(select(AuditOption).where(AuditOption.question_id == question_id)).all()
    for opt in existing:
        db.delete(opt)
    db.flush()
    for opt_in in options_in:
        db.add(AuditOption(
            question_id=question_id,
            label=opt_in.label,
            option_text=opt_in.option_text,
            weight=opt_in.weight,
        ))


# ---------------------------------------------------------------------------
# 6.2.1 — GET /questions/
# ---------------------------------------------------------------------------

@router.get("/", response_model=list[AuditQuestionPublic])
def list_questions(
    db: SessionDep,
    _admin: SuperuserDep,
    process: ProcessEnum | None = None,
    level: AspiceLevelEnum | None = None,
    is_active: bool | None = None,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """List all questions with optional filters. Admin only."""
    query = select(AuditQuestion)
    if process is not None:
        query = query.where(AuditQuestion.process == process)
    if level is not None:
        query = query.where(AuditQuestion.level == level)
    if is_active is not None:
        query = query.where(AuditQuestion.is_active == is_active)
    query = query.order_by(col(AuditQuestion.question_code)).offset(skip).limit(limit)
    questions = db.exec(query).all()
    return [_to_public(q, db) for q in questions]


# ---------------------------------------------------------------------------
# 6.2.2 — POST /questions/
# ---------------------------------------------------------------------------

@router.post("/", response_model=AuditQuestionPublic, status_code=201)
def create_question(
    question_in: QuestionIn,
    db: SessionDep,
    _admin: SuperuserDep,
) -> Any:
    """Create a question with its options and initialise its CMAB arm. Admin only."""
    existing = db.exec(
        select(AuditQuestion).where(AuditQuestion.question_code == question_in.question_code)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="question_code already exists")

    question = AuditQuestion(
        question_code=question_in.question_code,
        base_practice_id=question_in.base_practice_id,
        process=question_in.process,
        level=question_in.level,
        stakeholders=[r.value for r in question_in.stakeholders],
        question_text=question_in.question_text,
        recommendation_logic=question_in.recommendation_logic,
    )
    db.add(question)
    db.flush()  # get question.id

    for opt_in in question_in.options:
        db.add(AuditOption(
            question_id=question.id,
            label=opt_in.label,
            option_text=opt_in.option_text,
            weight=opt_in.weight,
        ))

    _init_bandit_arm(question.id, db)
    db.commit()
    db.refresh(question)
    return _to_public(question, db)


# ---------------------------------------------------------------------------
# 6.2.3 — PATCH /questions/{id}
# ---------------------------------------------------------------------------

@router.patch("/{question_id}", response_model=AuditQuestionPublic)
def update_question(
    question_id: int,
    question_in: QuestionUpdate,
    db: SessionDep,
    _admin: SuperuserDep,
) -> Any:
    """Update question fields. If `options` is provided, the full option set is replaced. Admin only."""
    question = _get_question_or_404(question_id, db)

    update_data = question_in.model_dump(exclude_unset=True, exclude={"options"})
    if "stakeholders" in update_data:
        update_data["stakeholders"] = [r.value for r in (question_in.stakeholders or [])]
    question.sqlmodel_update(update_data)
    db.add(question)

    if question_in.options is not None:
        _replace_options(question_id, question_in.options, db)

    db.commit()
    db.refresh(question)
    return _to_public(question, db)


# ---------------------------------------------------------------------------
# 6.2.4 — DELETE /questions/{id}  (soft delete)
# ---------------------------------------------------------------------------

@router.delete("/{question_id}", response_model=Message)
def deactivate_question(
    question_id: int,
    db: SessionDep,
    _admin: SuperuserDep,
) -> Any:
    """Soft-delete a question (sets is_active=False). BanditArmState is preserved. Admin only."""
    question = _get_question_or_404(question_id, db)
    question.is_active = False
    db.add(question)
    db.commit()
    return Message(message=f"Question {question_id} deactivated")


# ---------------------------------------------------------------------------
# 6.2.5 — POST /questions/seed  (bulk idempotent seed)
# ---------------------------------------------------------------------------

@router.post("/seed", response_model=SeedResult, status_code=201)
def seed_questions(
    payload: SeedIn,
    db: SessionDep,
    _admin: SuperuserDep,
) -> Any:
    """
    Bulk-insert questions. Questions whose `question_code` already exists are
    skipped (idempotent). Admin only.
    """
    inserted = 0
    skipped = 0

    for q_in in payload.questions:
        existing = db.exec(
            select(AuditQuestion).where(AuditQuestion.question_code == q_in.question_code)
        ).first()
        if existing:
            skipped += 1
            continue

        question = AuditQuestion(
            question_code=q_in.question_code,
            base_practice_id=q_in.base_practice_id,
            process=q_in.process,
            level=q_in.level,
            stakeholders=[r.value for r in q_in.stakeholders],
            question_text=q_in.question_text,
            recommendation_logic=q_in.recommendation_logic,
        )
        db.add(question)
        db.flush()

        for opt_in in q_in.options:
            db.add(AuditOption(
                question_id=question.id,
                label=opt_in.label,
                option_text=opt_in.option_text,
                weight=opt_in.weight,
            ))

        _init_bandit_arm(question.id, db)
        inserted += 1

    db.commit()
    return SeedResult(inserted=inserted, skipped=skipped)
