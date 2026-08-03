from typing import Any, Dict, List

class ValidationError(Exception):
    """Raised when a workout program fails validation."""
    pass

VALID_SET_TYPES = {"warmup", "normal", "failure", "dropset"}
VALID_RPES = {6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10}

def validate_program(program: Dict[str, Any], raise_on_error: bool = False) -> List[str]:
    """
    Validate a workout program definition.
    
    Args:
        program: A dictionary containing the program definition.
        raise_on_error: If True, raises ValidationError when errors are found.
        
    Returns:
        List of validation error strings.
    """
    errors: List[str] = []
    
    if not isinstance(program, dict):
        errors.append("Program must be a dictionary")
        if raise_on_error:
            raise ValidationError("Program validation failed:\n" + "\n".join(errors))
        return errors
        
    workouts = program.get("workouts")
    if not workouts or not isinstance(workouts, list):
        errors.append("Program must contain a non-empty 'workouts' list")
        if raise_on_error:
            raise ValidationError("Program validation failed:\n" + "\n".join(errors))
        return errors
        
    for i, workout in enumerate(workouts):
        _validate_workout(workout, i, errors)
        
    if errors and raise_on_error:
        raise ValidationError(f"Program validation failed with {len(errors)} errors:\n" + "\n".join(errors))
        
    return errors

def _validate_workout(workout: Dict[str, Any], index: int, errors: List[str]) -> None:
    title = workout.get("title")
    if not title or not isinstance(title, str) or not title.strip():
        errors.append(f"Workout at index {index} must have a non-empty 'title'")
        
    exercises = workout.get("exercises")
    if not exercises or not isinstance(exercises, list):
        errors.append(f"Workout '{title or index}' must have at least one exercise in 'exercises' list")
        return
        
    for j, exercise in enumerate(exercises):
        _validate_exercise(exercise, j, title or str(index), errors)

def _validate_exercise(exercise: Dict[str, Any], index: int, workout_title: str, errors: List[str]) -> None:
    name = exercise.get("name")
    if not name or not isinstance(name, str) or not name.strip():
        errors.append(f"Exercise at index {index} in workout '{workout_title}' must have a non-empty 'name'")
        
    sets = exercise.get("sets")
    if not sets or not isinstance(sets, list):
        errors.append(f"Exercise '{name or index}' in workout '{workout_title}' must have at least one set in 'sets' list")
        return
        
    for k, s in enumerate(sets):
        _validate_set(s, k, name or str(index), workout_title, errors)

def _validate_set(s: Dict[str, Any], index: int, exercise_name: str, workout_title: str, errors: List[str]) -> None:
    set_type = s.get("type", "normal")
    if set_type not in VALID_SET_TYPES:
        errors.append(f"Invalid set type '{set_type}' for set {index+1} of '{exercise_name}' in '{workout_title}'")
        
    weight = s.get("weight_kg")
    if weight is not None:
        if not isinstance(weight, (int, float)) or weight < 0:
            errors.append(f"Weight must be non-negative for set {index+1} of '{exercise_name}' in '{workout_title}'")
            
    reps = s.get("reps")
    if reps is not None:
        if not isinstance(reps, int) or reps < 0:
            errors.append(f"Reps must be non-negative integer for set {index+1} of '{exercise_name}' in '{workout_title}'")
            
    rpe = s.get("rpe")
    if rpe is not None:
        if rpe not in VALID_RPES:
            errors.append(f"Invalid RPE '{rpe}' for set {index+1} of '{exercise_name}' in '{workout_title}'. Valid values: {sorted(list(VALID_RPES))}")
