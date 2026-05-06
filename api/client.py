import requests
import logging

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json",
        })

    def get(self, endpoint: str, params: dict = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET {url} | params={params}")
        response = self.session.get(url, params=params)
        logger.info(f"Response: {response.status_code}")
        return response

    def post(self, endpoint: str, payload: dict) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST {url} | body={payload}")
        response = self.session.post(url, json=payload)
        logger.info(f"Response: {response.status_code} | {response.json()}")
        return response

    def put(self, endpoint: str, payload: dict) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT {url} | body={payload}")
        response = self.session.put(url, json=payload)
        logger.info(f"Response: {response.status_code}")
        return response

    def patch(self, endpoint: str, payload: dict) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PATCH {url} | body={payload}")
        response = self.session.patch(url, json=payload)
        logger.info(f"Response: {response.status_code}")
        return response

    def delete(self, endpoint: str) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE {url}")
        response = self.session.delete(url)
        logger.info(f"Response: {response.status_code}")
        return response
