from datetime import datetime, timedelta
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException,status
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from api.schema.delivery_partner import CreateDeliveryPartner, ReadDeliveryPartner
from database.models import DeliveryPartner
from database.session import session_db
from config import security_settings
from utils import generate_access_token

pwd_context = CryptContext(schemes=["argon2"],deprecated='auto')

class DeliveryPartnerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # async def get(self, id: int) ->  Shipment:
    #     return await self.session.get(Shipment,id)

    async def add(self,delivery_partner_create:CreateDeliveryPartner) ->  ReadDeliveryPartner:
        result = await self.session.execute(
            Select(DeliveryPartner).where(DeliveryPartner.email== delivery_partner_create.email)
        )
        if result.scalar_one_or_none() is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
        delivery_partner  = DeliveryPartner(
            **delivery_partner_create.model_dump(exclude=['password']),
            password_hash=pwd_context.hash(delivery_partner_create.password)
        )
        self.session.add(delivery_partner)
        await self.session.commit()
        await self.session.refresh(delivery_partner)
        return delivery_partner
    
    async def token(self, email, password)-> str:
        result = await self.session.execute(
            Select(DeliveryPartner).where(DeliveryPartner.email==email)
            )
        delivery_partner = result.scalar()
        self.session.get(DeliveryPartner,delivery_partner.id)
        verify_pass = pwd_context.verify(
            password,
            delivery_partner.password_hash
        )
        if delivery_partner is None or not verify_pass:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Email or password is incorrect")
        
        token = generate_access_token(data={
            "user":{
                "name": delivery_partner.name,
                'id': delivery_partner.id
            }
        })

        return token
        
        
async def get_delivery_service(session: session_db) -> DeliveryPartnerService:
    return DeliveryPartnerService(session)


delivery_partner_service = Annotated[DeliveryPartnerService, Depends(get_delivery_service)]