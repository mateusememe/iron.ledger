from typing import Dict, Any, List
from iron_ledger.api.client import HevyClient
from iron_ledger.constants import Endpoints

class FolderService:
    def __init__(self, client: HevyClient):
        self.client = client

    def create_folder(self, title: str) -> Dict[str, Any]:
        return self.client.post(Endpoints.ROUTINE_FOLDERS, json={"routine_folder": {"title": title}})

    def list_folders(self) -> List[Dict[str, Any]]:
        folders = []
        for page_data in self.client.get_paginated(Endpoints.ROUTINE_FOLDERS):
            if isinstance(page_data, dict) and "routine_folders" in page_data:
                folders.extend(page_data["routine_folders"])
            elif isinstance(page_data, list):
                folders.extend(page_data)
        return folders

    def get_folder(self, folder_id: str) -> Dict[str, Any]:
        endpoint = f"{Endpoints.ROUTINE_FOLDERS}/{folder_id}"
        return self.client.get(endpoint)
