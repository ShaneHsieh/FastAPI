from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    price: float = Field(..., gt=0)
    description: Optional[str] = None
    stock: int = Field(..., ge=0)
    category: Optional[str] = None
    discount: float = Field(..., ge=0, le=100)

class ProductCreate(ProductBase):
    supplier_ids: List[int] = []

class ProductUpdate(ProductBase):
    supplier_ids: Optional[List[int]] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductHistory(BaseModel):
    product_id: int
    price: float
    stock: int
    timestamp: datetime

class ProductHistoryResponse(ProductHistory):
    id: int

    class Config:
        from_attributes = True