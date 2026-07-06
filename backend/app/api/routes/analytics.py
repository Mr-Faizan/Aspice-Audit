"""
Analytics routes (all endpoints require superuser).

GET /analytics/weaknesses  — aggregate weakness heatmap across all completed sessions
GET /analytics/users       — user participation stats per stakeholder role
GET /analytics/bandit      — CMAB arm performance per question
"""
from collections import defaultdict
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import col, func, select

from app.api.deps import SessionDep, get_current_active_superuser
from app.models import (
    AuditSession,
    BanditArmState,
    AuditQuestion,
    SessionStatusEnum,
    StakeholderRoleEnum,
    User,
    WeaknessResult,
)

SuperuserDep = Annotated[Any, Depends(get_current_active_superuser)]

router = APIRouter()


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class WeaknessHeatmap(BaseModel):
    """Average weakness scores across all completed sessions, per (process, level)."""
    scores: dict[str, dict[str, float | None]]
    session_count: int


class RoleStats(BaseModel):
    role: str
    total_users: int
    sessions_started: int
    sessions_completed: int


class UsersAnalytics(BaseModel):
    roles: list[RoleStats]


class BanditArmStats(BaseModel):
    question_id: int
    question_code: str
    process: str
    level: str
    pull_count: int
    avg_reward: float | None


class BanditAnalytics(BaseModel):
    arms: list[BanditArmStats]


# ---------------------------------------------------------------------------
# 6.3.1 — GET /analytics/weaknesses
# ---------------------------------------------------------------------------

@router.get("/weaknesses", response_model=WeaknessHeatmap)
def aggregate_weaknesses(
    db: SessionDep,
    _admin: SuperuserDep,
) -> Any:
    """
    Average `WeaknessResult.scores` across all completed sessions.
    Returns an 18-cell heatmap (SWE1–SWE6 × L1–L3).
    Admin only.
    """
    results = db.exec(select(WeaknessResult)).all()

    if not results:
        # Return all-null heatmap when no sessions are completed yet
        empty: dict[str, dict[str, float | None]] = {
            p: {"L1": None, "L2": None, "L3": None}
            for p in ["SWE1", "SWE2", "SWE3", "SWE4", "SWE5", "SWE6"]
        }
        return WeaknessHeatmap(scores=empty, session_count=0)

    # Accumulate sum and count per (process, level) pair
    sums: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for wr in results:
        for process, levels in wr.scores.items():
            for level, score in levels.items():
                if score is not None:
                    sums[process][level] += score
                    counts[process][level] += 1

    processes = ["SWE1", "SWE2", "SWE3", "SWE4", "SWE5", "SWE6"]
    levels = ["L1", "L2", "L3"]
    heatmap: dict[str, dict[str, float | None]] = {}
    for p in processes:
        heatmap[p] = {}
        for lv in levels:
            n = counts[p].get(lv, 0)
            heatmap[p][lv] = sums[p][lv] / n if n > 0 else None

    return WeaknessHeatmap(scores=heatmap, session_count=len(results))


# ---------------------------------------------------------------------------
# 6.3.2 — GET /analytics/users
# ---------------------------------------------------------------------------

@router.get("/users", response_model=UsersAnalytics)
def user_stats(
    db: SessionDep,
    _admin: SuperuserDep,
) -> Any:
    """
    Return participation counts broken down by stakeholder role. Admin only.
    """
    roles = list(StakeholderRoleEnum)
    stats: list[RoleStats] = []

    for role in roles:
        user_ids = db.exec(
            select(User.id).where(User.stakeholder_role == role)
        ).all()

        total_users = len(user_ids)

        if not user_ids:
            stats.append(RoleStats(
                role=role.value,
                total_users=0,
                sessions_started=0,
                sessions_completed=0,
            ))
            continue

        sessions_started = db.exec(
            select(func.count(AuditSession.id))
            .where(col(AuditSession.user_id).in_(user_ids))
        ).one()

        sessions_completed = db.exec(
            select(func.count(AuditSession.id))
            .where(col(AuditSession.user_id).in_(user_ids))
            .where(AuditSession.status == SessionStatusEnum.completed)
        ).one()

        stats.append(RoleStats(
            role=role.value,
            total_users=total_users,
            sessions_started=sessions_started or 0,
            sessions_completed=sessions_completed or 0,
        ))

    return UsersAnalytics(roles=stats)


# ---------------------------------------------------------------------------
# 6.3.3 — GET /analytics/bandit
# ---------------------------------------------------------------------------

@router.get("/bandit", response_model=BanditAnalytics)
def bandit_performance(
    db: SessionDep,
    _admin: SuperuserDep,
) -> Any:
    """
    Return per-question CMAB arm statistics (pull count and average reward).
    Useful for thesis analysis and debugging. Admin only.
    """
    rows = db.exec(
        select(BanditArmState, AuditQuestion)
        .join(AuditQuestion, AuditQuestion.id == BanditArmState.question_id)
        .order_by(col(AuditQuestion.question_code))
    ).all()

    arms = [
        BanditArmStats(
            question_id=arm.question_id,
            question_code=question.question_code,
            process=question.process.value,
            level=question.level.value,
            pull_count=arm.pull_count,
            avg_reward=(arm.total_reward / arm.pull_count) if arm.pull_count > 0 else None,
        )
        for arm, question in rows
    ]

    return BanditAnalytics(arms=arms)
