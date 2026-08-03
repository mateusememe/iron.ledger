"""Tests for the exercise mapper module."""

from unittest.mock import MagicMock, patch
import pytest
from iron_ledger.domain.mapper import ExerciseMatcher


@pytest.fixture
def matcher():
    """Return an ExerciseMatcher instance loaded with sample templates."""
    matcher_inst = ExerciseMatcher()
    sample_templates = [
        {"id": "template_bench", "name": "Bench Press (Barbell)"},
        {"id": "template_squat", "name": "Squat (Barbell)"},
        {"id": "template_incline_db", "name": "Incline Dumbbell Press"},
        {"id": "template_deadlift", "name": "Deadlift (Barbell)"},
    ]
    matcher_inst.load_templates(sample_templates)
    return matcher_inst


def test_exact_match(matcher):
    """Test exact match returns correct template ID and score."""
    template_id, score = matcher.best_match("Bench Press (Barbell)")
    assert template_id == "template_bench"
    assert score >= 0.6


def test_case_insensitive_match(matcher):
    """Test matching exercise names with different casing."""
    template_id, score = matcher.best_match("bench press (barbell)")
    assert template_id == "template_bench"
    assert score >= 0.6


def test_fuzzy_match(matcher):
    """Test fuzzy matching for exercise name variations."""
    template_id, score = matcher.best_match("Incline DB Press")
    assert template_id == "template_incline_db"
    assert score >= 0.6


def test_no_match_below_threshold(matcher):
    """Test that queries with score below 0.6 threshold return None."""
    template_id, score = matcher.best_match("Unrelated Exercise XYZ 123")
    assert template_id is None
    assert score < 0.6


def test_normalize_removes_parentheses():
    """Test that normalize cleans input string and removes parentheses."""
    matcher_inst = ExerciseMatcher()
    normalized = matcher_inst.normalize("Bench Press (Barbell)")
    assert "(" not in normalized
    assert ")" not in normalized
    assert normalized == "bench press"


@patch("requests.get")
def test_load_templates_mocked_api(mock_get):
    """Test mocking API calls to fetch exercise templates."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {"id": "api_t1", "name": "Bench Press (Barbell)"},
            {"id": "api_t2", "name": "Barbell Squat"},
        ]
    }
    mock_get.return_value = mock_response

    matcher_inst = ExerciseMatcher()
    api_templates = mock_response.json()["data"]
    matcher_inst.load_templates(api_templates)

    template_id, score = matcher_inst.best_match("Bench Press")
    assert template_id == "api_t1"
    assert score >= 0.6
