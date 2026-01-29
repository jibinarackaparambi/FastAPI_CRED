from typing import Any

from fastapi import FastAPI, HTTPException, status

from schemas import CreateShipments, ReadShipmensts,UpdateShipments,PatchShipments


app = FastAPI()

shipments = {
  1001: {
    "content": "Electronics - Mobile Phones",
    "status": "In Transit",
    "weight": "12"
  },
  1002: {
    "content": "Books - Educational",
    "status": "Delivered",
    "weight": "8"
  },
  1003: {
    "content": "Clothing - Winter Jackets",
    "status": "Pending Pickup",
    "weight": "15"
  },
  1004: {
    "content": "Furniture - Office Chairs",
    "status": "In Transit",
    "weight": "25"
  },
  1005: {
    "content": "Groceries - Packaged Food",
    "status": "Delivered",
    "weight": "20"
  }
}

@app.get("/shipment", response_model=ReadShipmensts)
def get_shipments(id: int | None = None):
    if id is None or id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    return shipments[id]

@app.get('/shipment/{id}', response_model=ReadShipmensts)
def get_shipments_path_variable(id: int | None = None):
    if id is None or id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    return shipments[id]

@app.post('/shipment', response_model=None)
def create_shipment(request: CreateShipments):
    id = max(shipments.keys()) + 1
    shipments[id] = {
        **request.model_dump()
    }
    return {"shipment_id": id}

@app.put('/shipment/{id}',response_model=ReadShipmensts)
def update_shipments(shipment: UpdateShipments,id: int | None = None) -> dict[str,Any]:
    if id is None or id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    data = {
        **shipment.model_dump()
    }
    shipments[id].update(data)
    return shipments[id]

@app.patch('/shipment/{id}', response_model=None)
def patch_shipments(shipment: PatchShipments, id: int | None = None):
    if id is None or id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    shipments[id].update(**shipment.model_dump(exclude_none=True))
    return shipments[id]

@app.delete('/shipment/{id}')
def delete_shipments(id:int):
    if id is None or id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    pop_id = shipments.pop(id)
    return pop_id
  
