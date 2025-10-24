from sqlmodel import Session

from app.models import Promo, PromoCreate


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
