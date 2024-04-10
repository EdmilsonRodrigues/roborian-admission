from pydantic import BaseModel
from typing import Optional
from pymongo import GEOSPHERE


class Address(BaseModel):
    address_id: str
    address_line_1: str
    address_line_2: str
    city: str
    state: str
    country: str
    zip_code: str
    location: Optional[dict]

    class Config:
        orm_mode = True
        indexes = [{"fields": [("location", GEOSPHERE)]}]
    
    
    
    
