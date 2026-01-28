from typing import Any
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

shipments = {
  1001: {
    "content": "Electronics - Mobile Phones",
    "status": "In Transit",
    "weight": "12kg"
  },
  1002: {
    "content": "Books - Educational",
    "status": "Delivered",
    "weight": "8kg"
  },
  1003: {
    "content": "Clothing - Winter Jackets",
    "status": "Pending Pickup",
    "weight": "15kg"
  },
  1004: {
    "content": "Furniture - Office Chairs",
    "status": "In Transit",
    "weight": "25kg"
  },
  1005: {
    "content": "Groceries - Packaged Food",
    "status": "Delivered",
    "weight": "20kg"
  }
}

@app.get("/shipment")
def get_shipments(id: int | None = None) -> dict[str,Any]:
    if id is None or id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    return shipments[id]

@app.get('/shipment/{id}')
def get_shipments_path_variable(id: int | None = None) -> dict[str,Any]:
    if id is None or id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    return shipments[id]

@app.post('/shipment')
def create_shipment(request: dict[str,Any]) -> dict[str,int]:
    id = request.get('id', None)
    shipments[id] = {'content': request['content'], 'status': request['status'], 'weight': request['weight']}
    return {"id": id}