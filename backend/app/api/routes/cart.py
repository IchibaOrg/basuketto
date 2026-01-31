import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.api.deps import SessionDep
from app.models import (
    Cart,
    CartCreate,
    CartPublic,
    CartsPublic,
    CartUpdate,
    CartWithPromo,
    Message,
)
from app.repositories.cart import CartRepository
from app.repositories.cart_sqlmodel import SQLModelCartRepository

router = APIRouter(prefix="/carts", tags=["carts"])


def get_cart_repository(session: SessionDep) -> CartRepository:
    """
    Dependency factory that returns the repository implementation for the
    current request. Implementation is selected by the later implementation redis environment
    """
    return SQLModelCartRepository(session=session)


@router.delete("/{id}")
def delete_cart(
    id: uuid.UUID,
    repo: CartRepository = Depends(get_cart_repository),
) -> Message:
    """
    Delete a Cart.
    """
    return repo.delete(id=id)


@router.post("/", response_model=CartPublic)
def create_cart(
    cart_in: CartCreate,
    repo: CartRepository = Depends(get_cart_repository),
) -> Cart:
    """
    Create a Cart
    """
    return repo.create(cart_in=cart_in)


@router.put("/{id}", response_model=CartPublic)
def update_cart(
    id: uuid.UUID,
    cart_in: CartUpdate,
    repo: CartRepository = Depends(get_cart_repository),
) -> Cart:
    """
    Update a Cart
    """
    return repo.update(id=id, cart_in=cart_in)


@router.get("/{id}", response_model=CartWithPromo)
def read_cart(
    id: uuid.UUID,
    repo: CartRepository = Depends(get_cart_repository),
) -> Cart:
    """
    Get Cart by ID
    """
    return repo.get(id=id)


@router.get("/", response_model=CartsPublic)
def read_carts(
    skip: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    repo: CartRepository = Depends(get_cart_repository),
) -> Any:
    """
    Retrieve Carts
    """
    return repo.list(skip=skip, limit=limit)
