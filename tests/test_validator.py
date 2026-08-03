"""Tests for the program validator module."""

import pytest
from iron_ledger.importer.validator import validate_program


@pytest.fixture
def valid_program():
    """Return a valid workout program dictionary."""
    return {
        "name": "Hypertrophy Program",
        "workouts": [
            {
                "title": "Push Day",
                "exercises": [
                    {
                        "name": "Bench Press",
                        "sets": [
                            {
                                "type": "normal",
                                "reps": 8,
                                "weight_kg": 80.0,
                            }
                        ],
                    }
                ],
            }
        ],
    }


def test_valid_program_passes(valid_program):
    """Test that a valid program schema returns no errors."""
    errors = validate_program(valid_program)
    assert errors == []


def test_empty_title_fails(valid_program):
    """Test that a workout with an empty title produces validation errors."""
    valid_program["workouts"][0]["title"] = ""
    errors = validate_program(valid_program)
    assert len(errors) > 0


def test_no_exercises_fails(valid_program):
    """Test that a workout with no exercises produces validation errors."""
    valid_program["workouts"][0]["exercises"] = []
    errors = validate_program(valid_program)
    assert len(errors) > 0


def test_empty_exercise_name_fails(valid_program):
    """Test that an exercise with an empty name produces validation errors."""
    valid_program["workouts"][0]["exercises"][0]["name"] = ""
    errors = validate_program(valid_program)
    assert len(errors) > 0


def test_no_sets_fails(valid_program):
    """Test that an exercise with no sets produces validation errors."""
    valid_program["workouts"][0]["exercises"][0]["sets"] = []
    errors = validate_program(valid_program)
    assert len(errors) > 0


def test_invalid_set_type_fails(valid_program):
    """Test that an unrecognized set type produces validation errors."""
    valid_program["workouts"][0]["exercises"][0]["sets"][0]["type"] = "invalid_type"
    errors = validate_program(valid_program)
    assert len(errors) > 0


def test_negative_weight_fails(valid_program):
    """Test that a negative weight value produces validation errors."""
    valid_program["workouts"][0]["exercises"][0]["sets"][0]["weight_kg"] = -10.0
    errors = validate_program(valid_program)
    assert len(errors) > 0


def test_negative_reps_fails(valid_program):
    """Test that a negative reps value produces validation errors."""
    valid_program["workouts"][0]["exercises"][0]["sets"][0]["reps"] = -5
    errors = validate_program(valid_program)
    assert len(errors) > 0


def test_invalid_rpe_fails(valid_program):
    """Test that an out-of-bounds or invalid RPE value produces validation errors."""
    valid_program["workouts"][0]["exercises"][0]["sets"][0]["rpe"] = 15.0
    errors = validate_program(valid_program)
    assert len(errors) > 0


def test_valid_rpe_passes(valid_program):
    """Test that a valid RPE value passes validation."""
    valid_program["workouts"][0]["exercises"][0]["sets"][0]["rpe"] = 8.5
    errors = validate_program(valid_program)
    assert errors == []
