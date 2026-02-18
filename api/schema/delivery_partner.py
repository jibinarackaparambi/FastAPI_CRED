from typing import List
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import JSON, Column

class BaseDeliveryPartner(BaseModel):
    name: str
    email: EmailStr
    serviceable_zip_codes: List[int]
    max_handling_capacity: int
    

class CreateDeliveryPartner(BaseDeliveryPartner):
    password: str

class ReadDeliveryPartner(BaseDeliveryPartner):
    pass

