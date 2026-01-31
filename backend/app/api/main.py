from fastapi import APIRouter

from app.api.routes import cart, promo, utils

api_router = APIRouter()
api_router.include_router(utils.router)
api_router.include_router(promo.router)
api_router.include_router(cart.router)
