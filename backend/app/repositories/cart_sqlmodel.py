import uuid
from typing import Any

from fastapi import HTTPException
from sqlmodel import Session, func, select

from app.models import (
    Cart,
    CartCreate,
    CartPublic,
    CartsPublic,
    CartUpdate,
    Message,
    Promo,
)
from app.repositories.cart import CartRepository


class SQLModelCartRepository(CartRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def delete(self, id: uuid.UUID) -> Message:
        cart = self.session.get(Cart, id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        self.session.delete(cart)
        self.session.commit()
        return Message(message="Cart deleted successfully")

    def create(self, cart_in: CartCreate) -> Cart:
        cart = Cart.model_validate(cart_in)
        if cart.promo_id is not None:
            promo = self.session.get(Promo, cart.promo_id)
            if promo is None:
                raise HTTPException(status_code=400, detail="Invalid promo_id")
        self.session.add(cart)
        self.session.commit()
        self.session.refresh(cart)
        return cart

    def get(self, id: uuid.UUID) -> Cart:
        cart = self.session.get(Cart, id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        return cart

    def list(self, skip: int = 0, limit: int = 100) -> Any:
        count_statement = select(func.count()).select_from(Cart)
        count = self.session.exec(count_statement).one()
        statement = select(Cart).offset(skip).limit(limit)
        carts = self.session.exec(statement).all()
        carts_public = [CartPublic.model_validate(cart) for cart in carts]
        return CartsPublic(data=carts_public, count=count)

    def update(self, id: uuid.UUID, cart_in: CartUpdate) -> Cart:
        cart = self.session.get(Cart, id)
        if cart is None:
            raise HTTPException(status_code=404, detail="Cart not found")
        if cart_in.promo_id is not None:
            promo = self.session.get(Promo, cart_in.promo_id)
            if promo is None:
                raise HTTPException(status_code=400, detail="Invalid promo_id")
        update_dict = cart_in.model_dump(exclude_unset=True)
        cart.sqlmodel_update(update_dict)
        self.session.add(cart)
        self.session.commit()
        self.session.refresh(cart)
        return cart
