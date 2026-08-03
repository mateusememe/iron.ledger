import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from iron_ledger.config import Config, load_config
from iron_ledger.api.client import HevyClient
from iron_ledger.api.routines import RoutineService
from iron_ledger.api.folders import FolderService
from iron_ledger.api.exercises import ExerciseService
from iron_ledger.domain.mapper import ExerciseMatcher
from iron_ledger.domain.models import ExerciseSet, RoutineExercise, Routine
from iron_ledger.exceptions import MappingError
from .validator import validate_program

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ImportResult:
    workouts_created: int
    exercises_mapped: int
    folder_created: bool
    warnings: List[str] = field(default_factory=list)


class ProgramImporter:
    """Orchestrates the full import pipeline: validate → map → folder → routines."""

    def __init__(self, config: Optional[Config] = None) -> None:
        self.config = config or load_config()
        self._client = HevyClient(self.config)
        self.routine_service = RoutineService(self._client)
        self.folder_service = FolderService(self._client)
        self.exercise_service = ExerciseService(self._client)
        self.matcher = ExerciseMatcher(exercise_service=self.exercise_service)

    def import_program(
        self, program: Dict[str, Any], folder_name: Optional[str] = None
    ) -> ImportResult:
        name = program.get("name", "Unknown")
        logger.info(f"Starting import: {name}")

        # 1. Validate
        validate_program(program, raise_on_error=True)
        logger.info("✓ Validation passed")

        warnings: List[str] = []
        folder_id: Optional[int] = None

        # 2. Create folder (optional)
        folder_created = False
        if folder_name:
            result = self.folder_service.create_folder(folder_name)
            # API may return {"routine_folder": {...}} or {"id": ...} directly
            folder_data = result.get("routine_folder", result)
            folder_id = folder_data.get("id")
            folder_created = True
            logger.info(f"✓ Folder created: {folder_name} (id: {folder_id})")

        # 3. Map exercises and create routines
        exercises_mapped = 0
        workouts_created = 0

        for workout in program.get("workouts", []):
            routine_exercises: List[RoutineExercise] = []

            for exercise in workout.get("exercises", []):
                exercise_name = exercise["name"]
                template_id, score = self.matcher.best_match(exercise_name)

                if template_id is None:
                    warnings.append(f"No match for '{exercise_name}' (score: {score:.2f})")
                    raise MappingError(f"Could not map exercise: {exercise_name}")

                logger.info(f"✓ {exercise_name} → {template_id} ({score:.2f})")
                exercises_mapped += 1

                sets = [
                    ExerciseSet(
                        type=s.get("type", "normal"),
                        weight_kg=s.get("weight_kg"),
                        reps=s.get("reps"),
                    )
                    for s in exercise.get("sets", [])
                ]

                routine_exercises.append(
                    RoutineExercise(
                        exercise_template_id=template_id,
                        sets=sets,
                        rest_seconds=exercise.get("rest_seconds"),
                        notes=exercise.get("notes"),
                    )
                )

            routine = Routine(
                title=workout["title"],
                exercises=routine_exercises,
                folder_id=folder_id,
                notes=workout.get("notes"),
            )

            self.routine_service.create_routine(routine.to_dict())
            workouts_created += 1
            logger.info(f"✓ Routine created: {workout['title']}")

        logger.info(
            f"✓ Import complete. "
            f"{workouts_created} routines, {exercises_mapped} exercises."
        )

        return ImportResult(
            workouts_created=workouts_created,
            exercises_mapped=exercises_mapped,
            folder_created=folder_created,
            warnings=warnings,
        )
