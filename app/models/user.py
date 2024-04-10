from pydantic  import BaseModel, EmailStr
from typing import List, Optional
from .address import Address
from .contract import Contract
from pymongo import ASCENDING


class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: str
    communication_preferences: List[str]
    finances: str
    addresses: List[Address]
    contract: Optional[Contract]

    class Config:
        orm_mode = True
        indexes = [
            {
                "fields": [("email", ASCENDING)],
                "unique": True
            }
        ]
