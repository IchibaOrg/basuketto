from sqlmodel import Session

from app import crud
from app.models import DiscountType, Promo, PromoCreate
from app.tests.utils.utils import random_lower_string


def create_random_promo(db: Session) -> Promo:
    code = random_lower_string()
    discount_type = DiscountType.FIXED
    promo_in = PromoCreate(code=code, discount_type=discount_type, is_active=True)
    return crud.create_promo(session=db, promo_in=promo_in)
