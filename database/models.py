from datetime import datetime, timedelta
from enum import Enum
from pydantic import EmailStr
from sqlmodel import SQLModel, Field

class ShipmetStatus(str,Enum):
    placed = 'placed'
    in_transit = 'in_transit'
    out_for_delivery = 'out_for_delivery'
    delivered = 'delivered'
    
class Shipment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    content: str =  Field(max_length=30)
    weight: float  = Field(le=40,ge=1)
    status: ShipmetStatus
    estimated_delivery: datetime = Field(default=datetime.now() + timedelta(days=5))


class Seller(SQLModel,table=True):
    id: int = Field(default=None,primary_key=True)
    name: str
    email: EmailStr
    password_has: str