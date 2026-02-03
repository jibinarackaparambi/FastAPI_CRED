from datetime import datetime, timedelta
from typing import Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status

from schemas import CreateShipments, ReadShipmensts,UpdateShipments,PatchShipments
from database.models import Shipment,ShipmetStatus
from database.session import init_db,session_db

async def lifespan_handler(app:FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan_handler)

db = Shipment()

@app.get("/shipment", response_model=ReadShipmensts)
def get_shipments(session:session_db,id: int | None = None):
    print("@"*100)
    print(id)
    print("@"*100)
    shipment = session.get(Shipment,id)
    # shipment = db.get(id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    return shipment

# @app.get('/shipment/{id}', response_model=ReadShipmensts)
# def get_shipments_path_variable(id: int | None = None):
#     shipment = db.get(id)
#     if shipment is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
#     return shipment

@app.post('/shipment', response_model=None)
def create_shipment(request: CreateShipments,session: session_db):
    new_shipment = Shipment(
        **request.model_dump(),
        # estimated_delivery=datetime.now() + timedelta(days=5)
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)
    # new_id = db.create(request)
    return {"shipment_id": new_shipment.id}

@app.put('/shipment/{id}',response_model=ReadShipmensts)
def update_shipments(shipment_update: UpdateShipments,session: session_db,id: int | None = None) -> dict[str,Any]:
    # shipment = db.put(id,shipment)
    update = shipment_update.model_dump()
    if update is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Item not found")
    
    shipment = session.get(Shipment,id)
    shipment.sqlmodel_update(update)
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment

@app.patch('/shipment/{id}', response_model=None)
def patch_shipments(shipment_update: PatchShipments, session:session_db,id: int | None = None):
    # shipment = db.patch(id,shipment)
    update = shipment_update.model_dump(exclude_none=True)
    if id is None or update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    shipment = session.get(Shipment,id)
    shipment.sqlmodel_update(update)
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment

@app.delete('/shipment/{id}')
def delete_shipments(id:int, session:session_db):
    session.delete(
        session.get(Shipment,id)
    )
    session.commit()
    # shipment = db.delete(id)
    # if id is None or shipment is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    return {"details": f"#{id} deleted"}
  
