from dataclasses import dataclass, field
from typing import List, Optional

@dataclass(frozen=True)
class ExerciseTemplate:
    id: str
    title: str
    type: str
    primary_muscle_group: Optional[str] = None
    secondary_muscle_groups: List[str] = field(default_factory=list)
    equipment_category: Optional[str] = None
    is_custom: bool = False

@dataclass
class ExerciseSet:
    type: str  # warmup | normal | failure | dropset
    weight_kg: Optional[float] = None
    reps: Optional[int] = None
    distance_meters: Optional[float] = None
    duration_seconds: Optional[int] = None
    custom_metric: Optional[str] = None
    rep_range_start: Optional[int] = None
    rep_range_end: Optional[int] = None
    
    def to_dict(self) -> dict:
        data = {"type": self.type}
        if self.weight_kg is not None: data["weight_kg"] = self.weight_kg
        if self.reps is not None: data["reps"] = self.reps
        if self.distance_meters is not None: data["distance_meters"] = self.distance_meters
        if self.duration_seconds is not None: data["duration_seconds"] = self.duration_seconds
        if self.custom_metric is not None: data["custom_metric"] = self.custom_metric
        
        if self.rep_range_start is not None and self.rep_range_end is not None:
            data["rep_range"] = {"start": self.rep_range_start, "end": self.rep_range_end}
            
        return data

@dataclass
class RoutineExercise:
    exercise_template_id: str
    sets: List[ExerciseSet]
    superset_id: Optional[int] = None
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None
    
    def to_dict(self) -> dict:
        data = {
            "exercise_template_id": self.exercise_template_id,
            "sets": [s.to_dict() for s in self.sets]
        }
        if self.superset_id is not None: data["superset_id"] = self.superset_id
        if self.rest_seconds is not None: data["rest_seconds"] = self.rest_seconds
        if self.notes is not None: data["notes"] = self.notes
        return data

@dataclass
class Routine:
    title: str
    exercises: List[RoutineExercise]
    folder_id: Optional[int] = None
    notes: Optional[str] = None
    
    def to_dict(self) -> dict:
        data = {
            "title": self.title,
            "exercises": [e.to_dict() for e in self.exercises]
        }
        if self.folder_id is not None: data["folder_id"] = self.folder_id
        if self.notes is not None: data["notes"] = self.notes
        return data

@dataclass
class RoutineFolder:
    title: str
    
    def to_dict(self) -> dict:
        return {"title": self.title}
