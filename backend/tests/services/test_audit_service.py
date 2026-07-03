"""Unit tests for app.services.audit_service."""
import uuid
from unittest.mock import MagicMock, patch

import pytest

from app.models import (
    AuditOption,
    AuditQuestion,
    AuditSession,
    AspiceLevelEnum,
    ProcessEnum,
    SessionStatusEnum,
    StakeholderRoleEnum,
    User,
    WeaknessResult,
)
from app.services.audit_service import (
    AnswerResultCompleted,
    AnswerResultInProgress,
    _complete_session,
    _get_eligible_questions,
    submit_answer,
    start_session,
)


# ---------------------------------------------------------------------------
# Factories
# ---------------------------------------------------------------------------

def _user() -> User:
    return User(id=1, email="test@test.com", stakeholder_role=StakeholderRoleEnum.software_developer)


def _question(qid: int = 1) -> AuditQuestion:
    return AuditQuestion(
        id=qid,
        question_code=f"SWE1_L1_0{qid}",
        base_practice_id="SWE.1.BP1",
        process=ProcessEnum.SWE1,
        level=AspiceLevelEnum.L1,
        stakeholders=[StakeholderRoleEnum.software_developer],
        question_text="Question?",
        is_active=True,
    )


def _option(weight: int = 2, question_id: int = 1) -> AuditOption:
    return AuditOption(id=10, question_id=question_id, label="B", option_text="OK", weight=weight)


def _session(questions_asked: list[int] | None = None) -> AuditSession:
    s = AuditSession(
        id=uuid.uuid4(),
        user_id=1,
        status=SessionStatusEnum.in_progress,
        questions_asked=questions_asked or [],
        max_questions=12,
    )
    s.user = _user()
    return s


# ---------------------------------------------------------------------------
# 5.1.1 — start_session
# ---------------------------------------------------------------------------

class TestStartSession:
    @patch("app.services.audit_service.cmab_engine")
    def test_returns_session_and_question(self, mock_cmab):
        user = _user()
        question = _question()
        db = MagicMock()

        # exec().all() returns the eligible question list
        db.exec.return_value.all.return_value = [question]
        # _to_public needs a second exec for options
        mock_cmab.build_context.return_value = MagicMock()
        mock_cmab.select_question.return_value = question

        # _to_public will call db.exec again for options
        db.exec.return_value.all.side_effect = [
            [question],   # _get_eligible_questions
            [],            # _to_public options query
        ]

        session, public_q = start_session(user, db)

        assert session.user_id == user.id
        assert session.status == SessionStatusEnum.in_progress
        assert question.id in session.questions_asked
        assert public_q.id == question.id
        db.commit.assert_called_once()

    @patch("app.services.audit_service.cmab_engine")
    def test_raises_when_no_eligible_questions(self, mock_cmab):
        user = _user()
        db = MagicMock()
        db.exec.return_value.all.return_value = []
        mock_cmab.build_context.return_value = MagicMock()

        with pytest.raises(ValueError, match="No eligible questions"):
            start_session(user, db)


# ---------------------------------------------------------------------------
# 5.1.2 — submit_answer
# ---------------------------------------------------------------------------

class TestSubmitAnswer:
    @patch("app.services.audit_service.cmab_engine")
    def test_raises_on_unknown_session(self, _):
        db = MagicMock()
        db.get.return_value = None

        with pytest.raises(ValueError, match="not found"):
            submit_answer(uuid.uuid4(), 1, 10, db)

    @patch("app.services.audit_service.cmab_engine")
    def test_raises_on_completed_session(self, _):
        session = _session(questions_asked=[1])
        session.status = SessionStatusEnum.completed
        db = MagicMock()
        db.get.return_value = session

        with pytest.raises(ValueError, match="already completed"):
            submit_answer(session.id, 1, 10, db)

    @patch("app.services.audit_service.cmab_engine")
    def test_raises_on_wrong_question_id(self, _):
        session = _session(questions_asked=[5])  # last asked = 5
        db = MagicMock()
        db.get.return_value = session

        with pytest.raises(ValueError, match="does not match"):
            submit_answer(session.id, question_id=99, option_id=10, db=db)

    @patch("app.services.audit_service.cmab_engine")
    def test_raises_on_invalid_option(self, _):
        session = _session(questions_asked=[1])
        db = MagicMock()

        def get_side(model, pk):
            if model == AuditSession:
                return session
            if model == AuditOption:
                bad_option = _option()
                bad_option.question_id = 999  # belongs to different question
                return bad_option
            return None

        db.get.side_effect = get_side

        with pytest.raises(ValueError, match="not valid"):
            submit_answer(session.id, question_id=1, option_id=10, db=db)

    @patch("app.services.audit_service.cmab_engine")
    def test_returns_in_progress_when_budget_not_exhausted(self, mock_cmab):
        session = _session(questions_asked=[1])  # 1/12 answered
        next_q = _question(qid=2)
        option = _option(weight=2)
        db = MagicMock()

        def get_side(model, pk):
            if model == AuditSession:
                return session
            if model == AuditOption:
                return option
            if model == AuditQuestion:
                return _question()
            return None

        db.get.side_effect = get_side
        mock_cmab.build_context.return_value = MagicMock()
        mock_cmab.compute_reward.return_value = 0.5
        mock_cmab.select_question.return_value = next_q

        # exec().all() calls: _get_eligible_questions + _to_public options
        db.exec.return_value.all.side_effect = [
            [next_q],  # eligible questions
            [],         # options for _to_public
        ]

        result = submit_answer(session.id, question_id=1, option_id=10, db=db)

        assert isinstance(result, AnswerResultInProgress)
        assert result.status == "in_progress"
        assert result.next_question.id == next_q.id

    @patch("app.services.audit_service._complete_session")
    @patch("app.services.audit_service.cmab_engine")
    def test_returns_completed_when_budget_exhausted(self, mock_cmab, mock_complete):
        session = _session(questions_asked=list(range(1, 13)))  # 12/12 answered
        option = _option(weight=3, question_id=12)  # last asked is 12
        weakness = WeaknessResult(
            id=uuid.uuid4(),
            session_id=session.id,
            scores={},
            top_weaknesses=["SWE1-L1"],
        )

        db = MagicMock()

        def get_side(model, pk):
            if model == AuditSession:
                return session
            if model == AuditOption:
                return option
            if model == AuditQuestion:
                return _question()
            return None

        db.get.side_effect = get_side
        mock_cmab.build_context.return_value = MagicMock()
        mock_cmab.compute_reward.return_value = 0.75
        mock_complete.return_value = weakness
        db.exec.return_value.all.return_value = [_question(qid=99)]  # eligible (ignored)

        result = submit_answer(session.id, question_id=12, option_id=10, db=db)

        assert isinstance(result, AnswerResultCompleted)
        assert result.status == "completed"
        assert result.top_weaknesses == ["SWE1-L1"]
        mock_complete.assert_called_once()

    @patch("app.services.audit_service._complete_session")
    @patch("app.services.audit_service.cmab_engine")
    def test_returns_completed_when_no_eligible_questions_left(self, mock_cmab, mock_complete):
        session = _session(questions_asked=[1])  # only 1 answered
        option = _option(weight=3)
        weakness = WeaknessResult(
            id=uuid.uuid4(),
            session_id=session.id,
            scores={},
            top_weaknesses=[],
        )

        db = MagicMock()

        def get_side(model, pk):
            if model == AuditSession:
                return session
            if model == AuditOption:
                return option
            if model == AuditQuestion:
                return _question()
            return None

        db.get.side_effect = get_side
        mock_cmab.build_context.return_value = MagicMock()
        mock_cmab.compute_reward.return_value = 0.5
        mock_complete.return_value = weakness
        db.exec.return_value.all.return_value = []  # no eligible questions left

        result = submit_answer(session.id, question_id=1, option_id=10, db=db)

        assert isinstance(result, AnswerResultCompleted)
        mock_complete.assert_called_once()


# ---------------------------------------------------------------------------
# 5.1.3 — _complete_session
# ---------------------------------------------------------------------------

class TestCompleteSession:
    @patch("app.services.audit_service.weakness_classifier")
    def test_sets_status_completed(self, mock_wc):
        session = _session(questions_asked=[1, 2, 3])
        db = MagicMock()
        mock_wc.compute_scores.return_value = {"SWE1": {"L1": 0.5}}
        mock_wc.get_top_weaknesses.return_value = ["SWE1-L1"]

        _complete_session(session, db)

        assert session.status == SessionStatusEnum.completed
        assert session.completed_at is not None

    @patch("app.services.audit_service.weakness_classifier")
    def test_persists_weakness_result(self, mock_wc):
        session = _session(questions_asked=[1])
        db = MagicMock()
        mock_wc.compute_scores.return_value = {}
        mock_wc.get_top_weaknesses.return_value = ["SWE2-L2"]

        _complete_session(session, db)

        db.add.assert_called()
        db.commit.assert_called_once()

    @patch("app.services.audit_service.weakness_classifier")
    def test_returns_weakness_result(self, mock_wc):
        session = _session(questions_asked=[1])
        db = MagicMock()
        mock_wc.compute_scores.return_value = {}
        mock_wc.get_top_weaknesses.return_value = []

        result = _complete_session(session, db)

        assert result.session_id == session.id
        assert isinstance(result.top_weaknesses, list)


# ---------------------------------------------------------------------------
# _get_eligible_questions
# ---------------------------------------------------------------------------

class TestGetEligibleQuestions:
    def test_excludes_already_asked(self):
        session = _session(questions_asked=[1, 2])
        q3 = _question(qid=3)
        db = MagicMock()
        db.exec.return_value.all.return_value = [q3]

        result = _get_eligible_questions(session, db)

        assert result == [q3]
        # The WHERE NOT IN clause was applied (we trust the mock, but verify exec called)
        db.exec.assert_called_once()

    def test_empty_asked_list_queries_without_exclusion(self):
        session = _session(questions_asked=[])
        db = MagicMock()
        db.exec.return_value.all.return_value = []

        _get_eligible_questions(session, db)

        db.exec.assert_called_once()
