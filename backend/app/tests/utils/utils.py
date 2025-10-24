import random
import string

from fastapi.testclient import TestClient


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def get_superuser_token_headers(client: TestClient) -> None:
    """r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers"""
    pass
