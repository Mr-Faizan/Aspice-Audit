import uuid
from datetime import datetime, timezone
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.models import (
    Message,
    Question,
    QuestionCreate,
    QuestionPublic,
    Quiz,
    QuizCreate,
    QuizPublic,
    QuizStatusEnum,
    QuizUpdate,
    QuizWithQuestions,
    QuizzesPublic,
)

# All quiz admin routes require superuser (admin) access
SuperuserDep = Annotated[Any, Depends(get_current_active_superuser)]

router = APIRouter()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_quiz_or_404(session: SessionDep, quiz_id: uuid.UUID) -> Quiz:
    quiz = session.get(Quiz, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


def _quiz_to_public(quiz: Quiz) -> QuizPublic:
    """Convert a Quiz ORM object → QuizPublic, injecting question_count."""
    return QuizPublic(
        id=quiz.id,
        title=quiz.title,
        description=quiz.description,
        difficulty=quiz.difficulty,
        category=quiz.category,
        time_limit=quiz.time_limit,
        passing_score=quiz.passing_score,
        status=quiz.status,
        creator_id=quiz.creator_id,
        created_at=quiz.created_at,
        updated_at=quiz.updated_at,
        question_count=len(quiz.questions),
    )


def _create_questions(
    session: SessionDep,
    quiz_id: uuid.UUID,
    questions_in: list[QuestionCreate],
) -> None:
    """Persist a list of QuestionCreate schemas as Question rows."""
    for order, q_in in enumerate(questions_in):
        question = Question(
            quiz_id=quiz_id,
            question_text=q_in.question_text,
            options=q_in.options,
            correct_answer=q_in.correct_answer,
            explanation=q_in.explanation,
            points=q_in.points,
            order=order,
        )
        session.add(question)


# ---------------------------------------------------------------------------
# GET /quizzes  — list all quizzes (admin only)
# ---------------------------------------------------------------------------

@router.get("/", response_model=QuizzesPublic)
def read_quizzes(
    session: SessionDep,
    _admin: SuperuserDep,
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    category: str | None = None,
    difficulty: str | None = None,
) -> Any:
    """
    Retrieve all quizzes. Supports optional search, category and difficulty filters.
    Admin only.
    """
    base = select(Quiz)

    if search:
        base = base.where(col(Quiz.title).ilike(f"%{search}%"))
    if category:
        base = base.where(Quiz.category == category)
    if difficulty:
        base = base.where(col(Quiz.difficulty).cast(str) == difficulty)  # type: ignore[attr-defined]

    count_stmt = select(func.count()).select_from(base.subquery())
    count = session.exec(count_stmt).one()

    quizzes = session.exec(
        base.order_by(col(Quiz.created_at).desc()).offset(skip).limit(limit)
    ).all()

    data = [_quiz_to_public(q) for q in quizzes]
    return QuizzesPublic(data=data, count=count)


# ---------------------------------------------------------------------------
# POST /quizzes  — create quiz + questions
# ---------------------------------------------------------------------------

@router.post("/", response_model=QuizWithQuestions, status_code=201)
def create_quiz(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    _admin: SuperuserDep,
    quiz_in: QuizCreate,
) -> Any:
    """
    Create a new quiz with its questions. Admin only.
    """
    quiz = Quiz(
        title=quiz_in.title,
        description=quiz_in.description,
        difficulty=quiz_in.difficulty,
        category=quiz_in.category,
        time_limit=quiz_in.time_limit,
        passing_score=quiz_in.passing_score,
        creator_id=current_user.id,
    )
    session.add(quiz)
    session.flush()  # get quiz.id before creating questions

    _create_questions(session, quiz.id, quiz_in.questions)

    session.commit()
    session.refresh(quiz)

    return QuizWithQuestions(
        **_quiz_to_public(quiz).model_dump(),
        questions=[
            QuestionPublic(
                id=q.id,
                quiz_id=q.quiz_id,
                question_text=q.question_text,
                options=q.options,
                correct_answer=q.correct_answer,
                explanation=q.explanation,
                points=q.points,
                order=q.order,
            )
            for q in sorted(quiz.questions, key=lambda x: x.order)
        ],
    )


# ---------------------------------------------------------------------------
# PATCH /quizzes/{id}  — update quiz metadata + replace questions
# ---------------------------------------------------------------------------

@router.patch("/{id}", response_model=QuizWithQuestions)
def update_quiz(
    *,
    session: SessionDep,
    _admin: SuperuserDep,
    id: uuid.UUID,
    quiz_in: QuizUpdate,
) -> Any:
    """
    Update quiz metadata. If `questions` is provided the entire question set
    is replaced (delete-all + re-insert). Admin only.
    """
    quiz = _get_quiz_or_404(session, id)

    update_data = quiz_in.model_dump(exclude_unset=True, exclude={"questions"})
    update_data["updated_at"] = datetime.now(timezone.utc)
    quiz.sqlmodel_update(update_data)
    session.add(quiz)

    if quiz_in.questions is not None:
        # Delete all existing questions first
        for old_q in list(quiz.questions):
            session.delete(old_q)
        session.flush()
        _create_questions(session, quiz.id, quiz_in.questions)

    session.commit()
    session.refresh(quiz)

    return QuizWithQuestions(
        **_quiz_to_public(quiz).model_dump(),
        questions=[
            QuestionPublic(
                id=q.id,
                quiz_id=q.quiz_id,
                question_text=q.question_text,
                options=q.options,
                correct_answer=q.correct_answer,
                explanation=q.explanation,
                points=q.points,
                order=q.order,
            )
            for q in sorted(quiz.questions, key=lambda x: x.order)
        ],
    )


# ---------------------------------------------------------------------------
# DELETE /quizzes/{id}
# ---------------------------------------------------------------------------

@router.delete("/{id}", response_model=Message)
def delete_quiz(
    session: SessionDep,
    _admin: SuperuserDep,
    id: uuid.UUID,
) -> Any:
    """
    Delete a quiz (cascades to questions and attempts). Admin only.
    """
    quiz = _get_quiz_or_404(session, id)
    session.delete(quiz)
    session.commit()
    return Message(message="Quiz deleted successfully")


# ---------------------------------------------------------------------------
# PATCH /quizzes/{id}/publish  — toggle published / unpublished
# ---------------------------------------------------------------------------

@router.patch("/{id}/publish", response_model=QuizPublic)
def toggle_publish_quiz(
    session: SessionDep,
    _admin: SuperuserDep,
    id: uuid.UUID,
) -> Any:
    """
    Toggle a quiz between `published` and `unpublished` status.
    A quiz that is still `draft` will be moved to `published`.
    Admin only.
    """
    quiz = _get_quiz_or_404(session, id)

    if quiz.status == QuizStatusEnum.published:
        quiz.status = QuizStatusEnum.unpublished
    else:
        quiz.status = QuizStatusEnum.published

    quiz.updated_at = datetime.now(timezone.utc)
    session.add(quiz)
    session.commit()
    session.refresh(quiz)
    return _quiz_to_public(quiz)
