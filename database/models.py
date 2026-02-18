from typing import List, Optional
from datetime import datetime, timedelta
from enum import Enum
from pydantic import EmailStr
from sqlalchemy import JSON
from sqlmodel import SQLModel, Field, Relationship, Column

class ShipmetStatus(str,Enum):
    placed = 'placed'
    in_transit = 'in_transit'
    out_for_delivery = 'out_for_delivery'
    delivered = 'delivered'

class User(SQLModel):
    name: str
    email: EmailStr
    password_hash: str = Field(max_length=255, sa_column_kwargs={'nullable': False})

class Seller(User,table=True):
    __tablename__="seller"
    id: int = Field(default=None,primary_key=True)
    shipments: List["Shipment"] = Relationship(back_populates='owner')

class DeliveryPartner(User,  table=True):
    __tablename__= "delivery_partner"
    id: int = Field(default=None, primary_key=True)
    serviceable_zip_codes: List[int] = Field(default_factory=list, sa_column=Column(JSON)) 
    max_handling_capacity: int 
    shipments: List["Shipment"] = Relationship(back_populates='delivery_partners')

class Shipment(SQLModel, table=True):
    __tablename__="shipment"
    id: int = Field(default=None, primary_key=True)
    content: str =  Field(max_length=30)
    weight: float  = Field(le=40,ge=1)
    status: ShipmetStatus
    estimated_delivery: datetime = Field(default=datetime.now() + timedelta(days=5))

    destination: int = Field(default=None, nullable=True)

    owner_id: int = Field(foreign_key="seller.id",nullable=False)
    owner:Seller = Relationship(back_populates="shipments")

    delivery_prtner_id: Optional[int] = Field(foreign_key="delivery_partner.id")
    delivery_partners:DeliveryPartner = Relationship(back_populates="shipments")
    # delivery_partner: Optional["DeliveryPartner"] = Relationship(back_populates="shipments")  # Fixed 
