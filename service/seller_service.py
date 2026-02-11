from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException,status
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from api.schema.seller import CreateSeller, ReadSeller
from database.models import Seller
from config import security_settings
from utils import generate_access_token

pwd_context = CryptContext(schemes=["argon2"],deprecated='auto')

class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # async def get(self, id: int) ->  Shipment:
    #     return await self.session.get(Shipment,id)

    async def add(self,seller_create:CreateSeller) ->  ReadSeller:
        seller  = Seller(
            **seller_create.model_dump(exclude=['password']),
            password_hash=pwd_context.hash(seller_create.password)
        )
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller
    
    async def token(self, email, password)-> str:
        result = await self.session.execute(
            Select(Seller).where(Seller.email==email)
            )
        sellar = result.scalar()
        self.session.get(Seller,sellar.id)
        verify_pass = pwd_context.verify(
            password,
            sellar.password_hash
        )
        if sellar is None or not verify_pass:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Email or password is incorrect")
        
        token = generate_access_token(data={
            "user":{
                "name": sellar.name,
                'id': sellar.id
            }
        })

        return token
        
        

    