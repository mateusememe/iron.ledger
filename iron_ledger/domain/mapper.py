import re
import difflib
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from iron_ledger.domain.models import ExerciseTemplate
from iron_ledger.exceptions import MappingError

logger = logging.getLogger(__name__)


class ExerciseMatcher:
    def __init__(self, exercise_service=None):
        self.exercise_service = exercise_service
        self.templates: List[Union[ExerciseTemplate, Dict[str, Any]]] = []
        if self.exercise_service:
            self._load_from_service()

    def _load_from_service(self) -> None:
        if self.exercise_service:
            self.templates = self.exercise_service.list_templates()
            logger.info(f"Loaded {len(self.templates)} exercise templates for matching.")

    def load_templates(self, templates: list) -> None:
        """Load exercise templates from a list of dicts or ExerciseTemplate objects."""
        self.templates = templates
        logger.info(f"Loaded {len(self.templates)} exercise templates.")

    def normalize(self, name: str) -> str:
        """Normalize exercise name by removing parentheses, lowercasing, and stripping whitespace."""
        name = name.lower().strip()
        name = re.sub(r'\(.*?\)', '', name).strip()
        name = re.sub(r'\s+', ' ', name)
        return name

    def _get_template_info(self, template: Union[ExerciseTemplate, Dict[str, Any]]) -> Tuple[str, str]:
        if isinstance(template, dict):
            t_id = template.get("id", "")
            t_title = template.get("title") or template.get("name") or ""
        else:
            t_id = getattr(template, "id", "")
            t_title = getattr(template, "title", "") or getattr(template, "name", "")
        return t_id, t_title

    def best_match(self, name: str, threshold: float = 0.6) -> Tuple[Optional[str], float]:
        """Find the best template match for an exercise name.

        Strategy:
          1. Exact match on full name (case-insensitive).
          2. Fuzzy match on full name (preserving equipment in parentheses).
          3. Fallback: fuzzy match on normalized name (parentheses stripped).
        """
        target_lower = name.lower().strip()

        # --- Pass 1: exact match on full name ---
        for template in self.templates:
            t_id, t_title = self._get_template_info(template)
            if target_lower == t_title.lower().strip():
                logger.info(f"Matched '{name}' -> '{t_title}' (score: 1.00)")
                return t_id, 1.0

        # --- Pass 2: fuzzy match on full name (keeps parentheses) ---
        best_score = 0.0
        best_id: Optional[str] = None
        best_title = ""

        for template in self.templates:
            t_id, t_title = self._get_template_info(template)
            score = difflib.SequenceMatcher(
                None, target_lower, t_title.lower().strip()
            ).ratio()

            if score > best_score:
                best_score = score
                best_id = t_id
                best_title = t_title

        if best_id and best_score >= threshold:
            logger.info(f"Matched '{name}' -> '{best_title}' (score: {best_score:.2f})")
            return best_id, best_score

        # --- Pass 3: fuzzy match on normalized name (parentheses stripped) ---
        normalized_target = self.normalize(name)

        for template in self.templates:
            t_id, t_title = self._get_template_info(template)
            normalized_template = self.normalize(t_title)
            score = difflib.SequenceMatcher(
                None, normalized_target, normalized_template
            ).ratio()

            if score > best_score:
                best_score = score
                best_id = t_id
                best_title = t_title

        if best_id and best_score >= threshold:
            logger.info(f"Matched '{name}' -> '{best_title}' (score: {best_score:.2f})")
            return best_id, best_score

        logger.warning(f"No match found for '{name}' (best score: {best_score:.2f})")
        return None, best_score
