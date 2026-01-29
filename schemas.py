from enum import Enum

from pydantic import BaseModel, Field

class ShipmetStatus(str,Enum):
    placed = 'placed'
    in_transit = 'in_transit'
    out_for_delivery = 'out_for_delivery'
    delivered = 'delivered'

class BaseShipments(BaseModel):
    content: str = Field(max_length=30)
    weight: float = Field(le=40,ge=1)
    
class CreateShipments(BaseShipments):
    status: ShipmetStatus

class ReadShipmensts(BaseShipments):
    pass

class UpdateShipments(BaseShipments):
    status: ShipmetStatus

class PatchShipments(BaseModel):
    content: str | None = Field(max_length=30,default=None)
    weight: float | None = Field(le=40,ge=1,default=None)
    status: ShipmetStatus | None = Field(default="placed")
