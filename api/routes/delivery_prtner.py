from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from api.schema.delivery_partner import CreateDeliveryPartner, ReadDeliveryPartner
from core.security import delivery_partner_oauth2_scheme
from database.models import Seller
from database.redis import add_jti_to_blacklist
from database.session import session_db
from service.delivery_partner_service import DeliveryPartnerService, delivery_partner_service
from utils import decode_access_token, current_delivery_partner_dep


router = APIRouter(prefix="/delivery_partner",tags=['Delivery Partner'])

@router.post("/register", response_model=ReadDeliveryPartner)
async def register_delivery_partner(deliverty_partner:CreateDeliveryPartner,session: delivery_partner_service):
    # deliverty_partner =  await DeliveryPartnerService(session).add(deliverty_partner)
    deliverty_partner = await session.add(deliverty_partner)
    return deliverty_partner

@router.post("/token")
async def get_token(request_form:Annotated[OAuth2PasswordRequestForm,Depends()],session: delivery_partner_service):
    token = await session.token(request_form.username,request_form.password)
    return {
        "access_token":token,
        "access_type": "jwt"
    }

@router.get("/dashboard")
async def get_dashboard(token: Annotated[str, Depends(delivery_partner_oauth2_scheme)], session: session_db) -> ReadDeliveryPartner:
    data = decode_access_token(token=token)
    if data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid access token")
    seller = await session.get(Seller,data['user']['id'])
    return seller

@router.get('/logout')
async def logout_seller(token_data: Annotated[dict,Depends(current_delivery_partner_dep)]):
   await add_jti_to_blacklist(token_data['jti'])
   return {"details": "succesfully logged out"}