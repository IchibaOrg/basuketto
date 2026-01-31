from sqlmodel import Session

from app.models import Cart, CartCreate, Promo, PromoCreate


def create_promo(
    *,
    session: Session,
    promo_in: PromoCreate,
) -> Promo:
    db_promo = Promo.model_validate(
        promo_in,
    )
    session.add(db_promo)
    session.commit()
    session.refresh(db_promo)
    return db_promo


def create_cart(
    *,
    session: Session,
    cart_in: CartCreate,
) -> Cart:
    db_cart = Cart.model_validate(
        cart_in,
    )
    session.add(db_cart)
    session.commit()
    session.refresh(db_cart)
    return db_cart
