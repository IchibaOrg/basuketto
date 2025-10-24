import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.promo import create_random_promo


def test_create_promo(
    client: TestClient,
) -> None:
    data = {"code": "test_code", "discount_type": "fixed", "is_active": True}
    response = client.post(
        f"{settings.API_V1_STR}/promos/",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["code"] == data["code"]
    assert content["discount_type"] == data["discount_type"]
    assert "id" in content
    assert "discount_value" in content
    assert "is_active" in content


def test_read_promo(client: TestClient, db: Session) -> None:
    promo = create_random_promo(db)
    response = client.get(
        f"{settings.API_V1_STR}/promos/{promo.id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["code"] == promo.code
    assert content["discount_type"] == promo.discount_type
    assert content["id"] == str(promo.id)


def test_read_promo_not_found(
    client: TestClient,
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/promos/{uuid.uuid4()}",
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Promo not found"


""" def test_read_item_not_enough_permissions(client: TestClient, db: Session) -> None:
    promo = create_random_promo(db)
    response = client.get(
        f"{settings.API_V1_STR}/promos/{promo.id}",
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions" """


def test_read_promos(client: TestClient, db: Session) -> None:
    create_random_promo(db)
    create_random_promo(db)
    response = client.get(
        f"{settings.API_V1_STR}/promos/",
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_promo(client: TestClient, db: Session) -> None:
    promo = create_random_promo(db)
    data = {"code": "updated_code", "discount_type": "percent"}
    response = client.put(
        f"{settings.API_V1_STR}/promos/{promo.id}",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["code"] == data["code"]
    assert content["discount_type"] == data["discount_type"]
    assert content["id"] == str(promo.id)


def test_update_promo_not_found(
    client: TestClient,
) -> None:
    data = {"code": "updated_code", "discount_type": "percent"}
    response = client.put(
        f"{settings.API_V1_STR}/promos/{uuid.uuid4()}",
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Promo not found"


""" def test_update_promo_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    promo = create_random_promo(db)
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/promos/{promo.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions" """


def test_delete_promo(client: TestClient, db: Session) -> None:
    promo = create_random_promo(db)
    response = client.delete(
        f"{settings.API_V1_STR}/promos/{promo.id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Promo deleted successfully"


def test_delete_promos_not_found(
    client: TestClient,
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/promos/{uuid.uuid4()}",
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Promo not found"


""" def test_delete_item_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    response = client.delete(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions" """
