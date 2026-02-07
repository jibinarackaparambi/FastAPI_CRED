from typing import Any
from fastapi import APIRouter, HTTPException,status

from api.schema.schemas import CreateShipments, PatchShipments, ReadShipmensts, UpdateShipments
from database.models import Shipment
from database.session import session_db
from service.shipment_service import ShipmentService


router = APIRouter(tags=["Shipment"])


@router.get("/shipment")
async def get_shipments(session:session_db,id: int | None = None) -> Shipment:
    shipment = await ShipmentService(session).get(id)
    
    if id is None or shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    
    return shipment


@router.post('/shipment')
async def create_shipment(request: CreateShipments,session: session_db) -> Shipment:
    shipment = await ShipmentService(session).add(request)
    return shipment

@router.put('/shipment/{id}')
async def update_shipments(shipment_update: UpdateShipments,session: session_db,id: int | None = None) -> Shipment:
    shipment = await ShipmentService(session).put(shipment_update,id)
    return shipment

@router.patch('/shipment/{id}')
async def patch_shipments(shipment_update: PatchShipments, session:session_db,id: int | None = None) -> Shipment:
    shipment = await ShipmentService(session).patch(shipment_update,id)
    return shipment

@router.delete('/shipment/{id}')
async def delete_shipments(id:int, session:session_db):
    await ShipmentService(session).delete(id)
    return {"details": f" shipment with #{id} is deleted"}
  
