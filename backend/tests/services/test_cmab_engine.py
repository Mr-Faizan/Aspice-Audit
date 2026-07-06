"""Unit tests for app.services.cmab_engine.

These tests are pure-unit: they mock the DB session so no database
connection is required.
"""
import uuid
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from app.models import (
    AspiceLevelEnum,
    AuditOption,
    AuditQuestion,
    AuditSession,
    BanditArmState,
    ProcessEnum,
    SessionStatusEnum,
    StakeholderRoleEnum,
    User,
)
from app.services.cmab_engine import (
    _CONTEXT_DIM,
    _PROCESSES,
    build_context,
    compute_reward,
    select_question,
    update_arm,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_user(role: StakeholderRoleEnum = StakeholderRoleEnum.software_developer) -> User:
    return User(
        id=1,
        email="test@example.com",
        hashed_password="x",
        stakeholder_role=role,
    )


def _make_session(questions_asked: list[int] | None = None) -> AuditSession:
    return AuditSession(
        id=uuid.uuid4(),
        user_id=1,
        status=SessionStatusEnum.in_progress,
        questions_asked=questions_asked or [],
        max_questions=12,
        started_at=datetime.now(timezone.utc),
    )


def _make_question(
    qid: int = 1,
    process: ProcessEnum = ProcessEnum.SWE1,
    level: AspiceLevelEnum = AspiceLevelEnum.L1,
) -> AuditQuestion:
    return AuditQuestion(
        id=qid,
        question_code=f"SWE1_L1_0{qid}",
        base_practice_id="SWE.1.BP1",
        process=process,
        level=level,
        stakeholders=[],
        question_text="Placeholder question?",
    )


def _make_option(weight: int = 2, question_id: int = 1) -> AuditOption:
    return AuditOption(
        id=1,
        question_id=question_id,
        label="B",
        option_text="Some answer",
        weight=weight,
    )


def _mock_db() -> MagicMock:
    db = MagicMock()
    db.exec.return_value.all.return_value = []
    db.exec.return_value.first.return_value = None
    return db


# ---------------------------------------------------------------------------
# 3.3.1 — build_context
# ---------------------------------------------------------------------------

class TestBuildContext:
    def test_output_shape(self):
        db = _mock_db()
        user = _make_user()
        session = _make_session()
        ctx = build_context(session, user, db)
        assert ctx.shape == (_CONTEXT_DIM,), f"Expected ({_CONTEXT_DIM},), got {ctx.shape}"

    def test_one_hot_role_encoding(self):
        """Each role maps to exactly one non-zero position in [0:7]."""
        db = _mock_db()
        session = _make_session()
        for idx, role in enumerate(StakeholderRoleEnum):
            user = _make_user(role)
            ctx = build_context(session, user, db)
            assert ctx[idx] == 1.0
            assert ctx[:7].sum() == 1.0

    def test_progress_zero_at_start(self):
        db = _mock_db()
        ctx = build_context(_make_session([]), _make_user(), db)
        assert ctx[7] == 0.0

    def test_progress_half(self):
        # build_context calls db.exec(...).all() twice:
        #   1st: fetch questions by id list
        #   2nd: fetch (AuditResponse, AuditOption) rows
        questions = [_make_question(i + 1, ProcessEnum.SWE1, AspiceLevelEnum.L1) for i in range(6)]
        db = _mock_db()
        session = _make_session(list(range(6)))  # 6 of 12 asked
        db.exec.return_value.all.side_effect = [questions, []]
        ctx = build_context(session, _make_user(), db)
        assert ctx[7] == pytest.approx(0.5)

    def test_coverage_flags_empty_session(self):
        db = _mock_db()
        ctx = build_context(_make_session([]), _make_user(), db)
        assert ctx[8:17].sum() == 0.0  # no process or level flags set

    def test_all_values_in_valid_range(self):
        db = _mock_db()
        ctx = build_context(_make_session(), _make_user(), db)
        assert ctx.min() >= 0.0
        assert ctx.max() <= 1.0


# ---------------------------------------------------------------------------
# 3.3.2 — select_question
# ---------------------------------------------------------------------------

class TestSelectQuestion:
    def test_returns_question_from_eligible_list(self):
        db = _mock_db()
        questions = [_make_question(i) for i in range(1, 4)]
        result = select_question(np.zeros(_CONTEXT_DIM), questions, db)
        assert result in questions

    def test_single_eligible_question_always_selected(self):
        db = _mock_db()
        q = _make_question(1)
        result = select_question(np.zeros(_CONTEXT_DIM), [q], db)
        assert result is q

    def test_prefers_high_ucb_arm(self):
        """An arm with a large b vector should win over a fresh (identity) arm."""
        q_hot = _make_question(1)
        q_cold = _make_question(2)

        d = _CONTEXT_DIM
        hot_arm = BanditArmState(
            id=uuid.uuid4(),
            question_id=1,
            A_matrix=np.eye(d).tolist(),
            b_vector=(np.ones(d) * 10.0).tolist(),  # high theta
            pull_count=5,
            total_reward=4.0,
            updated_at=datetime.now(timezone.utc),
        )

        def fake_first_for(qid):
            return hot_arm if qid == 1 else None

        db = MagicMock()
        db.exec.return_value.first.side_effect = lambda: None  # default

        with patch("app.services.cmab_engine._load_or_init_arm") as mock_load:
            mock_load.side_effect = lambda qid, _db: (
                (np.array(hot_arm.A_matrix), np.array(hot_arm.b_vector))
                if qid == 1
                else (np.eye(d), np.zeros(d))
            )
            ctx = np.ones(d) / d  # uniform context
            result = select_question(ctx, [q_hot, q_cold], db)

        assert result is q_hot


# ---------------------------------------------------------------------------
# 3.3.3 — update_arm
# ---------------------------------------------------------------------------

class TestUpdateArm:
    def test_creates_arm_if_not_exists(self):
        db = _mock_db()
        ctx = np.zeros(_CONTEXT_DIM)
        ctx[0] = 1.0

        update_arm(42, ctx, 0.5, db)

        db.add.assert_called()
        db.commit.assert_called_once()

    def test_A_matrix_updated_correctly(self):
        """A_new = A_old + x·xᵀ"""
        d = _CONTEXT_DIM
        ctx = np.zeros(d)
        ctx[0] = 1.0

        existing_arm = BanditArmState(
            id=uuid.uuid4(),
            question_id=7,
            A_matrix=np.eye(d).tolist(),
            b_vector=np.zeros(d).tolist(),
            pull_count=0,
            total_reward=0.0,
            updated_at=datetime.now(timezone.utc),
        )

        db = MagicMock()
        db.exec.return_value.first.return_value = existing_arm

        update_arm(7, ctx, 0.8, db)

        A_new = np.array(existing_arm.A_matrix)
        expected = np.eye(d) + np.outer(ctx, ctx)
        np.testing.assert_allclose(A_new, expected)

    def test_b_vector_updated_correctly(self):
        """b_new = b_old + reward * x"""
        d = _CONTEXT_DIM
        ctx = np.zeros(d)
        ctx[2] = 1.0
        reward = 0.75

        existing_arm = BanditArmState(
            id=uuid.uuid4(),
            question_id=3,
            A_matrix=np.eye(d).tolist(),
            b_vector=np.zeros(d).tolist(),
            pull_count=0,
            total_reward=0.0,
            updated_at=datetime.now(timezone.utc),
        )

        db = MagicMock()
        db.exec.return_value.first.return_value = existing_arm

        update_arm(3, ctx, reward, db)

        b_new = np.array(existing_arm.b_vector)
        expected_b = np.zeros(d)
        expected_b[2] = reward
        np.testing.assert_allclose(b_new, expected_b)

    def test_pull_count_incremented(self):
        d = _CONTEXT_DIM
        existing_arm = BanditArmState(
            id=uuid.uuid4(),
            question_id=5,
            A_matrix=np.eye(d).tolist(),
            b_vector=np.zeros(d).tolist(),
            pull_count=3,
            total_reward=1.5,
            updated_at=datetime.now(timezone.utc),
        )
        db = MagicMock()
        db.exec.return_value.first.return_value = existing_arm

        update_arm(5, np.zeros(d), 0.5, db)

        assert existing_arm.pull_count == 4
        assert existing_arm.total_reward == pytest.approx(2.0)


# ---------------------------------------------------------------------------
# 3.3.4 — compute_reward
# ---------------------------------------------------------------------------

class TestComputeReward:
    def test_base_reward_weight_zero(self):
        db = _mock_db()
        option = _make_option(weight=0)
        question = _make_question(process=ProcessEnum.SWE1)
        session = _make_session([2, 3])  # SWE1 already covered — no bonus
        db.exec.return_value.all.return_value = [
            _make_question(2, ProcessEnum.SWE1),
            _make_question(3, ProcessEnum.SWE2),
        ]
        reward = compute_reward(option, question, session, db)
        assert reward == pytest.approx(0.0)

    def test_base_reward_max_weight(self):
        db = _mock_db()
        option = _make_option(weight=4)
        question = _make_question(process=ProcessEnum.SWE1)
        session = _make_session([2])
        db.exec.return_value.all.return_value = [_make_question(2, ProcessEnum.SWE1)]
        reward = compute_reward(option, question, session, db)
        assert reward == pytest.approx(1.0)

    def test_coverage_bonus_new_process(self):
        """Question introduces a new process → reward gets +0.2 bonus."""
        db = _mock_db()
        option = _make_option(weight=0)
        question = _make_question(process=ProcessEnum.SWE3)
        session = _make_session([1])
        # Only SWE1 covered so far
        db.exec.return_value.all.return_value = [_make_question(1, ProcessEnum.SWE1)]
        reward = compute_reward(option, question, session, db)
        assert reward == pytest.approx(0.2)

    def test_no_bonus_when_process_already_covered(self):
        db = _mock_db()
        option = _make_option(weight=2)
        question = _make_question(process=ProcessEnum.SWE2)
        session = _make_session([1])
        db.exec.return_value.all.return_value = [_make_question(1, ProcessEnum.SWE2)]
        reward = compute_reward(option, question, session, db)
        assert reward == pytest.approx(0.5)  # 2/4, no bonus

    def test_clamped_to_one(self):
        """weight=4 (reward=1.0) + coverage bonus → clamped to 1.0."""
        db = _mock_db()
        option = _make_option(weight=4)
        question = _make_question(process=ProcessEnum.SWE4)
        session = _make_session([1])
        db.exec.return_value.all.return_value = [_make_question(1, ProcessEnum.SWE1)]
        reward = compute_reward(option, question, session, db)
        assert reward == pytest.approx(1.0)

    def test_empty_session_always_gives_bonus(self):
        """First question of the session always earns the coverage bonus."""
        db = _mock_db()
        option = _make_option(weight=0)
        question = _make_question(process=ProcessEnum.SWE1)
        session = _make_session([])
        reward = compute_reward(option, question, session, db)
        assert reward == pytest.approx(0.2)
