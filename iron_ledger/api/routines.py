from typing import Dict, Any, List, Optional
from iron_ledger.api.client import HevyClient
from iron_ledger.constants import Endpoints

class RoutineService:
    def __init__(self, client: HevyClient):
        self.client = client

    def create_routine(self, routine_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.client.post(Endpoints.ROUTINES, json={"routine": routine_data})

    def list_routines(self) -> List[Dict[str, Any]]:
        routines = []
        for page_data in self.client.get_paginated(Endpoints.ROUTINES):
            if isinstance(page_data, dict) and "routines" in page_data:
                routines.extend(page_data["routines"])
            elif isinstance(page_data, list):
                routines.extend(page_data)
        return routines

    def get_routine(self, routine_id: str) -> Dict[str, Any]:
        endpoint = f"{Endpoints.ROUTINES}/{routine_id}"
        return self.client.get(endpoint)

    def update_routine(self, routine_id: str, routine_data: Dict[str, Any]) -> Dict[str, Any]:
        endpoint = f"{Endpoints.ROUTINES}/{routine_id}"
        return self.client.put(endpoint, json={"routine": routine_data})
