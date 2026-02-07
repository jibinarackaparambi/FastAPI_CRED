from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from api.schema.seller import CreateSeller
from database.models import Seller

pwd_context = CryptContext(schemes="bcrypt",deprecated='auto')
class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # async def get(self, id: int) ->  Shipment:
    #     return await self.session.get(Shipment,id)

    async def add(self,seller_create:CreateSeller) ->  Seller:
        seller  = Seller(
            **seller_create.model_dump(exclude=['password']),
            password_has=pwd_context.hash(seller_create.password)
        )
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller

    