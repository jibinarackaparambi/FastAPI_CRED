from typing import Any

from fastapi import FastAPI, HTTPException, status

from schemas import CreateShipments, ReadShipmensts,UpdateShipments,PatchShipments
from database import Shipment


app = FastAPI()

db = Shipment()

@app.get("/shipment", response_model=ReadShipmensts)
def get_shipments(id: int | None = None):
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    return shipment

@app.get('/shipment/{id}', response_model=ReadShipmensts)
def get_shipments_path_variable(id: int | None = None):
    shipment = db.get(id)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    return shipment

@app.post('/shipment', response_model=None)
def create_shipment(request: CreateShipments):
    new_id = db.create(request)
    return {"shipment_id": new_id}

@app.put('/shipment/{id}',response_model=ReadShipmensts)
def update_shipments(shipment: UpdateShipments,id: int | None = None) -> dict[str,Any]:
    shipment = db.put(id,shipment)
    if shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    return shipment

@app.patch('/shipment/{id}', response_model=None)
def patch_shipments(shipment: PatchShipments, id: int | None = None):
    shipment = db.patch(id,shipment)
    if id is None or shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    # shipments[id].update(**shipment.model_dump(exclude_none=True))
    return shipment

@app.delete('/shipment/{id}')
def delete_shipments(id:int):
    shipment = db.delete(id)
    if id is None or shipment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    return shipment
  
