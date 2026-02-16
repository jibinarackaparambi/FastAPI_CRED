from typing import List
from datetime import datetime, timedelta
from enum import Enum
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

class ShipmetStatus(str,Enum):
    placed = 'placed'
    in_transit = 'in_transit'
    out_for_delivery = 'out_for_delivery'
    delivered = 'delivered'


class Seller(SQLModel,table=True):
    id: int = Field(default=None,primary_key=True)
    name: str
    email: EmailStr
    password_hash: str = Field(max_length=255, sa_column_kwargs={'nullable': False})
    shipments: List["Shipment"] = Relationship(back_populates='owner')

class Shipment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    content: str =  Field(max_length=30)
    weight: float  = Field(le=40,ge=1)
    status: ShipmetStatus
    estimated_delivery: datetime = Field(default=datetime.now() + timedelta(days=5))
    owner_id: int = Field(foreign_key="seller.id",nullable=False)
    owner:Seller = Relationship(back_populates="shipments")