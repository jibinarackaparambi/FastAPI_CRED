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

@app.put('/shipment/{id}')
def update_shipments(content:str,status:str,weight:str ,id: int | None = None) -> dict[str,Any]:
    if id is None or id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    data = {
        'content': content, 
        'status': status, 
        'weight': weight
    }
    shipments[id].update(data)
    return shipments[id]

@app.patch('/shipment/{id}')
def patch_shipments(content:str | None = None,status:str | None = None,weight:str | None = None,id: int | None = None) -> dict[str,Any]:
    if id is None or id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    if content:
        shipments[id]['content'] = content
    if status:
        shipments[id]['status'] = status
    if weight:
        shipments[id]['weight'] = weight
    return shipments[id]