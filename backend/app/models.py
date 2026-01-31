import uuid
from decimal import Decimal
from enum import StrEnum

from sqlmodel import Field, Relationship, SQLModel


class DiscountType(StrEnum):
    PERCENT = "percent"
    FIXED = "fixed"


class Order(SQLModel, table=True):
    id: uuid.UUID | None = Field(primary_key=True, default_factory=uuid.uuid4)
    price: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    promo_id: uuid.UUID | None = Field(foreign_key="promo.id", default=None)


class CartBase(SQLModel):
    # total_price: Decimal = Field(default=0, ge=0, max_digits=6, decimal_places=2)
    promo_id: uuid.UUID | None = Field(default=None)


class CartCreate(CartBase):
    pass


class CartUpdate(CartBase):
    pass


class CartPublic(CartBase):
    id: uuid.UUID


class CartsPublic(SQLModel):
    data: list[CartPublic] = []
    count: int


class Cart(CartBase, table=True):
    id: uuid.UUID | None = Field(primary_key=True, default_factory=uuid.uuid4)
    # total_price: Decimal = Field(default=0, max_digits=6, decimal_places=2)
    promo_id: uuid.UUID | None = Field(foreign_key="promo.id", default=None)
    promo: "Promo" = Relationship(back_populates="carts")


class CartWithPromo(CartPublic):
    promo: "PromoPublic | None" = None


class PromoBase(SQLModel):
    code: str | None = Field(index=True, unique=True)
    discount_value: Decimal | None = Field(
        default=None, ge=0, max_digits=6, decimal_places=2
    )
    discount_type: DiscountType | None
    is_active: bool | None = Field(default=False)


class PromoCreate(PromoBase):
    pass


class PromoUpdate(PromoBase):
    code: str | None = None
    discount_value: Decimal | None = Field(default=None, ge=0)
    discount_type: DiscountType | None = None
    is_active: bool | None = False


class Promo(PromoBase, table=True):
    id: uuid.UUID | None = Field(primary_key=True, default_factory=uuid.uuid4)
    carts: list[Cart] = Relationship(back_populates="promo")


class PromoPublic(PromoBase):
    id: uuid.UUID


class PromosPublic(SQLModel):
    data: list[PromoPublic] = []
    count: int


class PromoWithCarts(PromoPublic):
    carts: list[CartPublic] = []


# Generic message
class Message(SQLModel):
    message: str
