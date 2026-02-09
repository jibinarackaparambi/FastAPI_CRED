from pydantic import BaseModel, EmailStr, Field

class BaseSeller(BaseModel):
    name: str
    email: EmailStr
    

class CreateSeller(BaseSeller):
    password: str

class ReadSeller(BaseSeller):
    pass

