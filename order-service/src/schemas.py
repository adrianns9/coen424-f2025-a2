from pydantic import BaseModel
from typing import List, Optional

class OrderItem(BaseModel):
    name: str
    quantity: int
    price: float

class OrderCreate(BaseModel):
    email: str
    delivery_address: str
    items: List[OrderItem]

class OrderUpdateStatus(BaseModel):
    status: str  # "under process", "shipping", "delivered"

class OrderUpdateContact(BaseModel):
    email: Optional[str] = None
    delivery_address: Optional[str] = None
