from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.db import engine
from app.main import app
from app.models import Cart, Order, Promo

# from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        statement = delete(Cart)
        session.execute(statement)
        statement = delete(Promo)
        session.execute(statement)
        statement = delete(Order)
        session.execute(statement)
        session.commit()


""" def override_get_db():
    pass """


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    # app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # app.dependency_overrides.clear()


""" @pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> None:
    return get_superuser_token_headers(client) """
