from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from api.schema.schemas import CreateShipments, PatchShipments, UpdateShipments
from database.models import Shipment

class ShipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) ->  Shipment:
        return await self.session.get(Shipment,id)

    async def add(self,shipment_create:CreateShipments) ->  Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
        )
        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)
        return new_shipment

    async def put(self, shipment_update: UpdateShipments, id: int) -> Shipment:
        shipment = await self.get(id)
        update = shipment_update.model_dump()

        if update is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Item not found")
        
        shipment.sqlmodel_update(update)
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment
    
    async def patch(self, shipment_patch: PatchShipments, id: int) -> Shipment:
        # shipment = db.patch(id,shipment)
        update = shipment_patch.model_dump(exclude_none=True)

        if id is None or update is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
        
        shipment = await self.get(id)
        shipment.sqlmodel_update(update)
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment

    async def delete(self,id: int) -> None:
        await self.session.delete(
        await self.get(id)
        )
        await self.session.commit() 