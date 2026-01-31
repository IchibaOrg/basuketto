import uuid

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.models import Cart, Promo
from app.tests.utils.cart import create_random_cart
from app.tests.utils.promo import create_random_promo


@pytest.fixture
def valid_promo(db: Session) -> Promo:
    return create_random_promo(db)


@pytest.fixture
def valid_cart(db: Session) -> Cart:
    return create_random_cart(db)


@pytest.mark.parametrize(
    "promo_id, extra_field, expected_status",
    [
        ("valid_promo", None, 200),  # valid promo
        ("efb4cac1-306d-4571-bf5e-49e8bab9e535", None, 400),  # nonexistent promo
        ("", None, 422),  # invalid promo
        (None, None, 200),  # no promo
        (None, "unknown", 200),  # no promo, unknown extra field
    ],
)
def test_create_cart_parametrized(
    client: TestClient,
    request,
    promo_id,
    extra_field,
    expected_status,
) -> None:
    if promo_id == "valid_promo":
        promo = request.getfixturevalue(promo_id)
        promo_id = str(promo.id)
    data = {"promo_id": promo_id}
    if extra_field:
        data["unknown"] = extra_field
    response = client.post(f"{settings.API_V1_STR}/carts/", json=data)
    assert response.status_code == expected_status
    if expected_status == 200:
        content = response.json()
        assert content["promo_id"] == promo_id
        assert "id" in content
        assert "unknown" not in content


def test_read_cart(client: TestClient, valid_cart: Cart) -> None:
    response = client.get(f"{settings.API_V1_STR}/carts/{valid_cart.id}")
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == str(valid_cart.id)
    assert content["promo_id"] == str(valid_cart.promo_id)


def test_read_cart_not_found(
    client: TestClient,
) -> None:
    response = client.get(f"{settings.API_V1_STR}/carts/{uuid.uuid4()}")
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Cart not found"


def test_read_carts(client: TestClient, db: Session) -> None:
    create_random_cart(db)
    create_random_cart(db)
    response = client.get(f"{settings.API_V1_STR}/carts/")
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_read_carts_with_limit(client: TestClient, db: Session) -> None:
    create_random_cart(db)
    create_random_cart(db)
    create_random_cart(db)
    limit = 2
    response = client.get(f"{settings.API_V1_STR}/carts/?limit={limit}")
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == limit


def test_read_carts_with_skip(client: TestClient, db: Session) -> None:
    create_random_cart(db)
    create_random_cart(db)
    create_random_cart(db)
    create_random_cart(db)
    skip = 2
    full_resp = client.get(f"{settings.API_V1_STR}/carts/")
    response = client.get(f"{settings.API_V1_STR}/carts/?skip={skip}")
    assert response.status_code == 200
    full_content = full_resp.json()["data"]
    skip_content = response.json()["data"]
    assert full_content[skip:] == skip_content


def test_update_cart(client: TestClient, valid_cart: Cart) -> None:
    data = {"promo_id": None}
    response = client.put(f"{settings.API_V1_STR}/carts/{valid_cart.id}", json=data)
    assert response.status_code == 200
    content = response.json()
    assert content["promo_id"] == data["promo_id"]
    assert content["id"] == str(valid_cart.id)


def test_update_nonexistent_cart(client: TestClient) -> None:
    data = {"promo_id": None}
    response = client.put(
        f"{settings.API_V1_STR}/carts/efb4cac1-306d-4571-bf5e-49e8bab9e535", json=data
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Cart not found"


def test_update_cart_with_extra_fields(client: TestClient, db: Session) -> None:
    cart = create_random_cart(db)
    data = {"promo_id": None, "unknown_field": "value"}
    response = client.put(f"{settings.API_V1_STR}/carts/{cart.id}", json=data)
    assert response.status_code == 200
    content = response.json()
    assert content["promo_id"] == data["promo_id"]
    assert content["id"] == str(cart.id)


def test_update_cart_invalid_promo_id(client: TestClient, valid_cart: Cart) -> None:
    data = {"promo_id": ""}
    response = client.put(f"{settings.API_V1_STR}/carts/{valid_cart.id}", json=data)
    assert response.status_code == 422
    content = response.json()
    assert "uuid" in content["detail"][0]["type"]
    assert "promo_id" in content["detail"][0]["loc"]


def test_update_cart_nonexistent_promo_id(client: TestClient, db: Session) -> None:
    cart = create_random_cart(db)
    data = {"promo_id": "efb4cac1-306d-4571-bf5e-49e8bab9e535"}
    response = client.put(f"{settings.API_V1_STR}/carts/{cart.id}", json=data)
    assert response.status_code == 400
    content = response.json()
    assert "promo_id" in content["detail"]


def test_delete_cart(client: TestClient, valid_cart: Cart) -> None:
    response = client.delete(f"{settings.API_V1_STR}/carts/{valid_cart.id}")
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Cart deleted successfully"


def test_delete_cart_not_found(
    client: TestClient,
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/carts/{uuid.uuid4()}",
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Cart not found"
