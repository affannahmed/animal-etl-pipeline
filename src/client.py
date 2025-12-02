import requests
from typing import Dict, Any, List
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


class AnimalAPIClient:
    def __init__(self, base_url: str = "http://localhost:3123") -> None:
        self.base_url = base_url
        self.session = requests.Session()

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type((requests.exceptions.RequestException,)),
    )
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, timeout=60, **kwargs)

        if response.status_code in [500, 502, 503, 504]:
            print(f"Server error {response.status_code}, retrying wait for server to respond")
            response.raise_for_status()

        response.raise_for_status()
        return response.json()

    def get_animals_page(self, page: int = 1) -> Dict[str, Any]:
        """Fetch a single page of animals."""
        return self._make_request("GET", f"/animals/v1/animals?page={page}")

    def get_animal_details(self, animal_id: int) -> Dict[str, Any]:
        """Fetch details for a specific animal."""
        return self._make_request("GET", f"/animals/v1/animals/{animal_id}")

    def post_animals(self, animals_batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Post a batch of animals to /home endpoint."""
        return self._make_request("POST", "/animals/v1/home", json=animals_batch)
