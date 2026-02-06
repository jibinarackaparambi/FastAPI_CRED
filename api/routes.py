from typing import Any
from fastapi import APIRouter, HTTPException,status

from api.schema.schemas import CreateShipments, PatchShipments, ReadShipmensts, UpdateShipments
from database.models import Shipment
from database.session import session_db


router = APIRouter()


@router.get("/shipment", response_model=ReadShipmensts)
async def get_shipments(session:session_db,id: int | None = None):
    shipment = await session.get(Shipment,id)
    if id is None or shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    
    # shipment = db.get(id)
    return shipment


@router.post('/shipment', response_model=None)
async def create_shipment(request: CreateShipments,session: session_db):
    new_shipment = Shipment(
        **request.model_dump(),
        # estimated_delivery=datetime.now() + timedelta(days=5)
    )
    session.add(new_shipment)
    await session.commit()
    await session.refresh(new_shipment)
    # new_id = db.create(request)
    return {"shipment_id": new_shipment.id}

@router.put('/shipment/{id}',response_model=ReadShipmensts)
async def update_shipments(shipment_update: UpdateShipments,session: session_db,id: int | None = None) -> dict[str,Any]:
    # shipment = db.put(id,shipment)
    shipment = await session.get(Shipment,id)
    update = shipment_update.model_dump()
    if update is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Item not found")
    
    
    shipment.sqlmodel_update(update)
    session.add(shipment)
    await session.commit()
    await session.refresh(shipment)
    return shipment

@router.patch('/shipment/{id}', response_model=None)
async def patch_shipments(shipment_update: PatchShipments, session:session_db,id: int | None = None):
    # shipment = db.patch(id,shipment)
    update = shipment_update.model_dump(exclude_none=True)
    if id is None or update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    shipment = await session.get(Shipment,id)
    shipment.sqlmodel_update(update)
    session.add(shipment)
    await session.commit()
    await session.refresh(shipment)
    return shipment

@router.delete('/shipment/{id}')
async def delete_shipments(id:int, session:session_db):
    await session.delete(
        await session.get(Shipment,id)
    )
    await session.commit()
    # shipment = db.delete(id)
    # if id is None or shipment is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    return {"details": f"#{id} deleted"}
  
