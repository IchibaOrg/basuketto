import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import func, select

from app.api.deps import SessionDep
from app.models import (
    Message,
    Promo,
    PromoCreate,
    PromoPublic,
    PromosPublic,
    PromoUpdate,
)

router = APIRouter(prefix="/promos", tags=["promos"])


@router.get("/", response_model=PromosPublic)
def read_promos(
    session: SessionDep, skip: int = 0, limit: int = Query(default=100, le=100)
) -> Any:
    """
    Retrieve promos.
    """
    count_statement = select(func.count()).select_from(Promo)
    count = session.exec(count_statement).one()
    statement = select(Promo).offset(skip).limit(limit)
    promos = session.exec(statement).all()
    promos_public = [PromoPublic.model_validate(promo) for promo in promos]
    return PromosPublic(data=promos_public, count=count)


@router.get("/{id}", response_model=PromoPublic)
def read_promo(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get promo by ID.
    """
    promo = session.get(Promo, id)
    if not promo:
        raise HTTPException(status_code=404, detail="Promo not found")
    return promo


@router.post("/", response_model=PromoPublic)
def create_promo(*, session: SessionDep, promo_in: PromoCreate) -> Any:
    """
    Create new promo.
    """
    promo = Promo.model_validate(promo_in)
    session.add(promo)
    session.commit()
    session.refresh(promo)
    return promo


@router.put("/{id}", response_model=PromoPublic)
def update_promo(
    *,
    session: SessionDep,
    id: uuid.UUID,
    promo_in: PromoUpdate,
) -> Any:
    """
    Update a promo.
    """
    promo = session.get(Promo, id)
    if not promo:
        raise HTTPException(status_code=404, detail="Promo not found")
    update_dict = promo_in.model_dump(exclude_unset=True)
    promo.sqlmodel_update(update_dict)
    session.add(promo)
    session.commit()
    session.refresh(promo)
    return promo


@router.delete("/{id}")
def delete_promo(session: SessionDep, id: uuid.UUID) -> Message:
    """
    Delete a Promo.
    """
    promo = session.get(Promo, id)
    if not promo:
        raise HTTPException(status_code=404, detail="Promo not found")
    session.delete(promo)
    session.commit()
    return Message(message="Promo deleted successfully")
