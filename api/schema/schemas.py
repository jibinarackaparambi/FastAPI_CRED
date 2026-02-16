from datetime import datetime, timedelta
from pydantic import BaseModel, Field

from database.models import ShipmetStatus


class BaseShipments(BaseModel):
    content: str = Field(max_length=30)
    weight: float = Field(le=40,ge=1)
    estimated_delivery:datetime = Field(default=datetime.now() + timedelta(days=5))
    
class CreateShipments(BaseShipments):
    status: ShipmetStatus
    owner_id: int = Field(default=None)

class ReadShipmensts(BaseShipments):
    pass

class UpdateShipments(BaseShipments):
    status: ShipmetStatus

class PatchShipments(BaseModel):
    content: str | None = Field(max_length=30,default=None)
    weight: float | None = Field(le=40,ge=1,default=None)
    status: ShipmetStatus | None = Field(default=None)
    estimated_delivery:datetime |None = Field(default=None)
