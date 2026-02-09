from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from api.schema.seller import CreateSeller, ReadSeller
from database.models import Seller

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

    