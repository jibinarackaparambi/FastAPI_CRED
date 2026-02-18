from fastapi import APIRouter
from .routes import shipment, seller, delivery_prtner

master_router = APIRouter()

master_router.include_router(shipment.router)
master_router.include_router(seller.router)
master_router.include_router(delivery_prtner.router)