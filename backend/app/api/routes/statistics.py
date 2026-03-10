from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends
from sqlmodel import col, func, select

from app.api.deps import get_current_active_superuser, SessionDep
from app.models import (
    PopularQuizPublic,
    Quiz,
    QuizAttempt,
    QuizStatisticsPublic,
    QuizStatusEnum,
    RecentAttemptPublic,
    StatisticsPublic,
    User,
    UserStatisticsPublic,
)

router = APIRouter()

# All statistics routes require admin access
AdminDep = Depends(get_current_active_superuser)


@router.get("/", response_model=StatisticsPublic, dependencies=[AdminDep])
def get_dashboard_summary(*, session: SessionDep) -> Any:
    """
    Get general dashboard summary stats.
    """
    # Total Users
    total_users = session.exec(select(func.count()).select_from(User)).one()
    active_users = session.exec(
        select(func.count()).select_from(User).where(User.is_active == True)
    ).one()

    # Quizzes
    total_quizzes = session.exec(select(func.count()).select_from(Quiz)).one()
    published_quizzes = session.exec(
        select(func.count()).select_from(Quiz).where(Quiz.status == QuizStatusEnum.published)
    ).one()
    unpublished_quizzes = total_quizzes - published_quizzes

    # Attempts
    total_attempts = session.exec(select(func.count()).select_from(QuizAttempt)).one()
    
    # Average Score
    avg_score = session.exec(select(func.avg(QuizAttempt.score))).one() or 0.0

    # Recent Attempts
    recent_attempts_stmt = (
        select(QuizAttempt, Quiz.title, User.full_name, User.email)
        .join(Quiz, QuizAttempt.quiz_id == Quiz.id)
        .join(User, QuizAttempt.user_id == User.id)
        .order_by(col(QuizAttempt.completed_at).desc())
        .limit(5)
    )
    recent_attempts_raw = session.exec(recent_attempts_stmt).all()
    
    recent_attempts = [
        RecentAttemptPublic(
            id=attempt.id,
            quiz_id=attempt.quiz_id,
            quiz_title=quiz_title,
            user_id=attempt.user_id,
            user_full_name=user_full_name,
            user_email=user_email,
            score=attempt.score,
            passed=attempt.passed,
            completed_at=attempt.completed_at
        )
        for attempt, quiz_title, user_full_name, user_email in recent_attempts_raw
    ]

    return StatisticsPublic(
        total_users=total_users,
        active_users=active_users,
        total_quizzes=total_quizzes,
        published_quizzes=published_quizzes,
        unpublished_quizzes=unpublished_quizzes,
        total_attempts=total_attempts,
        average_score=float(avg_score),
        recent_attempts=recent_attempts
    )


@router.get("/users", response_model=UserStatisticsPublic, dependencies=[AdminDep])
def get_user_statistics(*, session: SessionDep) -> Any:
    """
    Get detailed user metrics.
    """
    total_users = session.exec(select(func.count()).select_from(User)).one()
    active_users = session.exec(
        select(func.count()).select_from(User).where(User.is_active == True)
    ).one()
    
    # New users this month
    start_of_month = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    new_users = session.exec(
        select(func.count()).select_from(User).where(User.created_at >= start_of_month)
    ).one()

    admin_users = session.exec(
        select(func.count()).select_from(User).where(User.is_superuser == True)
    ).one()
    regular_users = total_users - admin_users

    return UserStatisticsPublic(
        total_users=total_users,
        active_users=active_users,
        new_users_this_month=new_users,
        admin_users=admin_users,
        regular_users=regular_users
    )


@router.get("/quizzes", response_model=QuizStatisticsPublic, dependencies=[AdminDep])
def get_quiz_statistics(*, session: SessionDep) -> Any:
    """
    Get detailed quiz metrics.
    """
    total_quizzes = session.exec(select(func.count()).select_from(Quiz)).one()
    published_quizzes = session.exec(
        select(func.count()).select_from(Quiz).where(Quiz.status == QuizStatusEnum.published)
    ).one()
    unpublished_quizzes = total_quizzes - published_quizzes

    # Quizzes by Category
    categories_raw = session.exec(select(Quiz.category, func.count(Quiz.id)).group_by(Quiz.category)).all()
    quizzes_by_category = {cat: count for cat, count in categories_raw}

    # Quizzes by Difficulty
    diff_raw = session.exec(select(Quiz.difficulty, func.count(Quiz.id)).group_by(Quiz.difficulty)).all()
    quizzes_by_difficulty = {str(diff.value): count for diff, count in diff_raw}

    # Average attempts per quiz
    total_attempts = session.exec(select(func.count()).select_from(QuizAttempt)).one()
    avg_attempts = total_attempts / total_quizzes if total_quizzes > 0 else 0

    # Most popular quizzes
    popular_stmt = (
        select(Quiz.id, Quiz.title, func.count(QuizAttempt.id).label("attempts"))
        .join(QuizAttempt, Quiz.id == QuizAttempt.quiz_id)
        .group_by(Quiz.id, Quiz.title)
        .order_by(col("attempts").desc())
        .limit(5)
    )
    popular_raw = session.exec(popular_stmt).all()
    most_popular_quizzes = [
        PopularQuizPublic(id=id, title=title, attempts=attempts)
        for id, title, attempts in popular_raw
    ]

    return QuizStatisticsPublic(
        total_quizzes=total_quizzes,
        published_quizzes=published_quizzes,
        unpublished_quizzes=unpublished_quizzes,
        quizzes_by_category=quizzes_by_category,
        quizzes_by_difficulty=quizzes_by_difficulty,
        average_attempts_per_quiz=float(avg_attempts),
        most_popular_quizzes=most_popular_quizzes
    )
