from sqlmodel import Session

from app import crud
from app.models import Cart, CartCreate
from app.tests.utils.promo import create_random_promo


def create_random_cart(db: Session) -> Cart:
    promo = create_random_promo(db)
    cart_in = CartCreate(promo_id=promo.id)
    return crud.create_cart(session=db, cart_in=cart_in)
