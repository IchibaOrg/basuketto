import uuid
from abc import ABC, abstractmethod

from app.models import Cart, CartCreate, CartsPublic, CartUpdate, Message


class CartRepository(ABC):
    @abstractmethod
    def get(self, id: uuid.UUID) -> Cart:
        pass

    @abstractmethod
    def create(self, cart_in: CartCreate) -> Cart:
        pass

    @abstractmethod
    def update(self, id: uuid.UUID, cart_in: CartUpdate) -> Cart:
        pass

    @abstractmethod
    def delete(self, id: uuid.UUID) -> Message:
        pass

    @abstractmethod
    def list(self, skip: int = 0, limit: int = 100) -> CartsPublic:
        pass
