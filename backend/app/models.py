import uuid
from decimal import Decimal
from enum import StrEnum

from sqlmodel import Field, SQLModel


class DiscountType(StrEnum):
    PERCENT = "percent"
    FIXED = "fixed"


class Order(SQLModel, table=True):
    id: uuid.UUID | None = Field(primary_key=True, default_factory=uuid.uuid4)
    price: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    promo_id: uuid.UUID | None = Field(foreign_key="promo.id", default=None)


class Cart(SQLModel, table=True):
    id: uuid.UUID | None = Field(primary_key=True, default_factory=uuid.uuid4)
    total_price: Decimal = Field(default=0, max_digits=6, decimal_places=2)
    promo_id: uuid.UUID | None = Field(foreign_key="promo.id", default=None)


class PromoBase(SQLModel):
    code: str | None = Field(default=None, index=True)
    discount_value: Decimal = Field(default=0, ge=0, max_digits=6, decimal_places=2)
    discount_type: DiscountType
    is_active: bool = True


class PromoCreate(PromoBase):
    pass


class PromoUpdate(PromoBase):
    code: str | None = None
    discount_value: Decimal | None = Field(default=None, ge=0)  # type: ignore
    discount_type: DiscountType | None = None  # type: ignore
    is_active: bool | None = None  # type: ignore


class Promo(PromoBase, table=True):
    id: uuid.UUID | None = Field(primary_key=True, default_factory=uuid.uuid4)


class PromoPublic(PromoBase):
    id: uuid.UUID


class PromosPublic(SQLModel):
    data: list[PromoPublic] = []
    count: int


# Generic message
class Message(SQLModel):
    message: str
