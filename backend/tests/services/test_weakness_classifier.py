"""Unit tests for app.services.weakness_classifier."""
import uuid
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from app.models import (
    AspiceLevelEnum,
    AuditOption,
    AuditQuestion,
    AuditResponse,
    ProcessEnum,
)
from app.services.weakness_classifier import (
    classify,
    compute_scores,
    get_top_weaknesses,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_row(process: ProcessEnum, level: AspiceLevelEnum, weight: int):
    """Simulate one joined row (AuditResponse, AuditOption, AuditQuestion)."""
    response = AuditResponse(
        id=uuid.uuid4(),
        session_id=uuid.uuid4(),
        question_id=1,
        option_id=1,
        answered_at=datetime.now(timezone.utc),
    )
    option = AuditOption(id=1, question_id=1, label="B", option_text="x", weight=weight)
    question = AuditQuestion(
        id=1,
        question_code="SWE1_L1_01",
        base_practice_id="SWE.1.BP1",
        process=process,
        level=level,
        stakeholders=[],
        question_text="?",
    )
    return response, option, question


def _db_with_rows(rows: list) -> MagicMock:
    db = MagicMock()
    db.exec.return_value.all.return_value = rows
    return db


# ---------------------------------------------------------------------------
# 4.2 — compute_scores
# ---------------------------------------------------------------------------

class TestComputeScores:
    def test_returns_all_18_pairs(self):
        db = _db_with_rows([])
        scores = compute_scores(uuid.uuid4(), db)
        assert len(scores) == 6  # 6 processes
        for process_scores in scores.values():
            assert len(process_scores) == 3  # 3 levels each

    def test_null_when_no_responses(self):
        db = _db_with_rows([])
        scores = compute_scores(uuid.uuid4(), db)
        for process_scores in scores.values():
            for score in process_scores.values():
                assert score is None

    def test_single_response_correct_score(self):
        """One answer with weight 2 → score = 2/4 = 0.5."""
        rows = [_make_row(ProcessEnum.SWE1, AspiceLevelEnum.L1, weight=2)]
        db = _db_with_rows(rows)
        scores = compute_scores(uuid.uuid4(), db)
        assert scores["SWE1"]["L1"] == pytest.approx(0.5)

    def test_mean_of_multiple_responses(self):
        """Two answers (weight 0 and weight 4) → mean = 0.5."""
        rows = [
            _make_row(ProcessEnum.SWE2, AspiceLevelEnum.L2, weight=0),
            _make_row(ProcessEnum.SWE2, AspiceLevelEnum.L2, weight=4),
        ]
        db = _db_with_rows(rows)
        scores = compute_scores(uuid.uuid4(), db)
        assert scores["SWE2"]["L2"] == pytest.approx(0.5)

    def test_other_pairs_remain_null(self):
        """Only SWE3-L1 is answered; all other pairs should still be null."""
        rows = [_make_row(ProcessEnum.SWE3, AspiceLevelEnum.L1, weight=3)]
        db = _db_with_rows(rows)
        scores = compute_scores(uuid.uuid4(), db)
        assert scores["SWE3"]["L1"] == pytest.approx(0.75)
        assert scores["SWE3"]["L2"] is None
        assert scores["SWE1"]["L1"] is None

    def test_max_weight_gives_score_one(self):
        rows = [_make_row(ProcessEnum.SWE6, AspiceLevelEnum.L3, weight=4)]
        db = _db_with_rows(rows)
        scores = compute_scores(uuid.uuid4(), db)
        assert scores["SWE6"]["L3"] == pytest.approx(1.0)

    def test_min_weight_gives_score_zero(self):
        rows = [_make_row(ProcessEnum.SWE1, AspiceLevelEnum.L1, weight=0)]
        db = _db_with_rows(rows)
        scores = compute_scores(uuid.uuid4(), db)
        assert scores["SWE1"]["L1"] == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# 4.2 — classify
# ---------------------------------------------------------------------------

class TestClassify:
    def test_none_is_not_assessed(self):
        assert classify(None) == "not_assessed"

    def test_zero_is_compliant(self):
        assert classify(0.0) == "compliant"

    def test_boundary_0_25_is_compliant(self):
        assert classify(0.25) == "compliant"

    def test_just_above_0_25_is_minor_weakness(self):
        assert classify(0.26) == "minor_weakness"

    def test_boundary_0_50_is_minor_weakness(self):
        assert classify(0.50) == "minor_weakness"

    def test_just_above_0_50_is_significant_gap(self):
        assert classify(0.51) == "significant_gap"

    def test_boundary_0_75_is_significant_gap(self):
        assert classify(0.75) == "significant_gap"

    def test_just_above_0_75_is_critical_gap(self):
        assert classify(0.76) == "critical_gap"

    def test_one_is_critical_gap(self):
        assert classify(1.0) == "critical_gap"

    def test_all_four_categories_reachable(self):
        categories = {classify(s) for s in [0.0, 0.3, 0.6, 0.9]}
        assert categories == {"compliant", "minor_weakness", "significant_gap", "critical_gap"}


# ---------------------------------------------------------------------------
# 4.2 — get_top_weaknesses
# ---------------------------------------------------------------------------

class TestGetTopWeaknesses:
    def _scores(self, overrides: dict) -> dict:
        """Build a full 6×3 scores dict with all nulls, then apply overrides."""
        scores: dict = {}
        for p in ["SWE1", "SWE2", "SWE3", "SWE4", "SWE5", "SWE6"]:
            scores[p] = {"L1": None, "L2": None, "L3": None}
        for key, value in overrides.items():
            process, level = key.split("-")
            scores[process][level] = value
        return scores

    def test_returns_top_3_by_default(self):
        scores = self._scores({"SWE1-L1": 0.9, "SWE2-L2": 0.6, "SWE3-L1": 0.4, "SWE4-L2": 0.1})
        result = get_top_weaknesses(scores)
        assert result == ["SWE1-L1", "SWE2-L2", "SWE3-L1"]

    def test_sorted_descending(self):
        scores = self._scores({"SWE5-L3": 0.3, "SWE6-L1": 0.8, "SWE1-L2": 0.5})
        result = get_top_weaknesses(scores)
        assert result[0] == "SWE6-L1"
        assert result[1] == "SWE1-L2"
        assert result[2] == "SWE5-L3"

    def test_null_pairs_excluded(self):
        scores = self._scores({"SWE1-L1": 0.9})  # all others are null
        result = get_top_weaknesses(scores)
        assert result == ["SWE1-L1"]

    def test_n_parameter_respected(self):
        scores = self._scores({"SWE1-L1": 0.9, "SWE2-L1": 0.8, "SWE3-L1": 0.7, "SWE4-L1": 0.6})
        assert len(get_top_weaknesses(scores, n=2)) == 2
        assert len(get_top_weaknesses(scores, n=4)) == 4

    def test_empty_scores_returns_empty_list(self):
        scores = self._scores({})
        assert get_top_weaknesses(scores) == []

    def test_fewer_pairs_than_n(self):
        scores = self._scores({"SWE2-L2": 0.5})
        result = get_top_weaknesses(scores, n=3)
        assert result == ["SWE2-L2"]  # only 1 assessed, should not error
