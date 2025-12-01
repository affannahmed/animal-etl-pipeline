import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


class AnimalAPIClient:

    
    def __init__(self, base_url="http://localhost:3123"):
        self.base_url = base_url
        self.session = requests.Session()
    
    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type((requests.exceptions.RequestException,))
    )
    def _make_request(self, method, endpoint, **kwargs):

        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, timeout=60, **kwargs)

        if response.status_code in [500, 502, 503, 504]:
            print(f"Server error {response.status_code}, retrying wait for server to responsd")
            response.raise_for_status()
        
        response.raise_for_status()
        return response.json()
    
    def get_animals_page(self, page=1):
        """Fetch a single page of animals."""
        return self._make_request("GET", f"/animals/v1/animals?page={page}")
    
    def get_animal_details(self, animal_id):
        """Fetch details for a specific animal."""
        return self._make_request("GET", f"/animals/v1/animals/{animal_id}")
    
    def post_animals(self, animals_batch):
        """Post a batch of animals to /home endpoint."""
        return self._make_request("POST", "/animals/v1/home", json=animals_batch)