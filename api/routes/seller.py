from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api.schema.seller import CreateSeller, ReadSeller
from database.session import session_db
from service.seller_service import SellerService

router = APIRouter(prefix="/seller",tags=['seller'])

@router.post("/register", response_model=ReadSeller)
async def register_seller(seller:CreateSeller,session: session_db):
    seller =  await SellerService(session).add(seller)
    return seller

@router.post("/token")
async def get_token(request_form:Annotated[OAuth2PasswordRequestForm,Depends()],session: session_db):
    token = await SellerService(session).token(request_form.username,request_form.password)
    return {
        "access_token":token,
        "access_type": "jwt"
    }