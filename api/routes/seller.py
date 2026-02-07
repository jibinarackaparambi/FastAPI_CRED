from fastapi import APIRouter

from api.schema.seller import CreateSeller, ReadSeller
from database.session import session_db
from service.seller_service import SellerService

router = APIRouter(prefix="/seller",tags=['seller'])

@router.post("/register", response_model=ReadSeller)
async def register_seller(seller:CreateSeller,session: session_db):
    seller =  await SellerService(session).add(seller)
    return seller