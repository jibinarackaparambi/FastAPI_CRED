from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException,status

from api.schema.schemas import CreateShipments, PatchShipments, ReadShipmensts, UpdateShipments
from database.models import Shipment
from database.redis import add_jti_to_blacklist
from database.session import session_db
from service.shipment_service import ShipmentService
from utils import get_access_token,current_seller_dep


router = APIRouter(tags=["Shipment"])


@router.get("/shipment")
async def get_shipments(session:session_db,seller_db: current_seller_dep,id: int | None = None) -> Shipment:
    shipment = await ShipmentService(session).get(id)
    
    if id is None or shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    
    return shipment


@router.post('/shipment')
async def create_shipment(request: CreateShipments,session: session_db, seller_db: current_seller_dep) -> Shipment:
    print(seller_db)
    # await add_jti_to_blacklist(current_seller_dep['jti'])
    
    shipment = await ShipmentService(session).add(request)
    return shipment

@router.put('/shipment/{id}')
async def update_shipments(shipment_update: UpdateShipments,seller_db: current_seller_dep,session: session_db,id: int | None = None) -> Shipment:
    shipment = await ShipmentService(session).put(shipment_update,id)
    return shipment

@router.patch('/shipment/{id}')
async def patch_shipments(shipment_update: PatchShipments,seller_db: current_seller_dep, session:session_db,id: int | None = None) -> Shipment:
    shipment = await ShipmentService(session).patch(shipment_update,id)
    return shipment

@router.delete('/shipment/{id}')
async def delete_shipments(id:int, session:session_db, seller_db: current_seller_dep):
    await ShipmentService(session).delete(id)
    return {"details": f" shipment with #{id} is deleted"}
  
