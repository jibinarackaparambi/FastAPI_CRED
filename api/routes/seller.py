from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.schema.seller import CreateSeller, ReadSeller
from core.security import oauth2_scheme
from database.models import Seller
from database.redis import add_jti_to_blacklist
from database.session import session_db
from service.seller_service import SellerService
from utils import decode_access_token, get_access_token


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

@router.get("/dashboard")
async def get_dashboard(token: Annotated[str, Depends(oauth2_scheme)], session: session_db) -> ReadSeller:
    data = decode_access_token(token=token)
    if data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid access token")
    seller = await session.get(Seller,data['user']['id'])
    return seller

@router.get('/logout')
async def logout_seller(token_data: Annotated[dict,Depends(get_access_token)]):
   await add_jti_to_blacklist(token_data['jti'])
   return {"details": "succesfully logged out"}