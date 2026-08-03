from typing import Dict, Any, List
from iron_ledger.api.client import HevyClient
from iron_ledger.constants import Endpoints
from iron_ledger.domain.models import ExerciseTemplate

class ExerciseService:
    def __init__(self, client: HevyClient):
        self.client = client

    def list_templates(self) -> List[ExerciseTemplate]:
        templates = []
        for page_data in self.client.get_paginated(Endpoints.EXERCISE_TEMPLATES):
            items = []
            if isinstance(page_data, dict) and "exercise_templates" in page_data:
                items = page_data["exercise_templates"]
            elif isinstance(page_data, list):
                items = page_data
                
            for item in items:
                templates.append(
                    ExerciseTemplate(
                        id=item.get("id"),
                        title=item.get("title", ""),
                        type=item.get("type", ""),
                        primary_muscle_group=item.get("primary_muscle_group"),
                        secondary_muscle_groups=item.get("secondary_muscle_groups", []),
                        equipment_category=item.get("equipment_category"),
                        is_custom=item.get("is_custom", False)
                    )
                )
        return templates

    def get_template(self, template_id: str) -> Dict[str, Any]:
        endpoint = f"{Endpoints.EXERCISE_TEMPLATES}/{template_id}"
        return self.client.get(endpoint)
