import requests
from typing import Dict, Any, Generator, Optional
from urllib.parse import urljoin

from iron_ledger.config import Config
from iron_ledger.constants import BASE_URL
from iron_ledger.exceptions import ApiError
from iron_ledger.utils.retry import with_retry


class HevyClient:
    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "api-key": self.config.hevy_api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        self.base_url = BASE_URL

    @with_retry
    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        url = urljoin(self.base_url, endpoint)
        response = self.session.request(method, url, **kwargs)

        if not response.ok:
            error_body = None
            try:
                error_body = response.json()
            except ValueError:
                pass

            detail = error_body.get("error", "") if error_body else response.text
            raise ApiError(
                f"{response.status_code} {response.reason}: {detail}",
                status_code=response.status_code,
                response=error_body,
            )

        if response.content:
            return response.json()
        return None

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("POST", endpoint, json=json)

    def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("PUT", endpoint, json=json)

    def get_paginated(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None, page_size: int = 10
    ) -> Generator[Dict[str, Any], None, None]:
        params = dict(params or {})
        params["pageSize"] = page_size
        page = 1

        while True:
            params["page"] = page
            data = self.get(endpoint, params=params)

            if not isinstance(data, dict):
                yield data
                break

            yield data

            page_count = data.get("page_count", 1)
            if page >= page_count:
                break
            page += 1
