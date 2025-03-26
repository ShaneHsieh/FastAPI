from pydantic import BaseModel, Field
from typing import List, Optional

class SupplierBase(BaseModel):
    name: str = Field(..., min_length=1)
    contact_info: Optional[str] = None
    rating: float = Field(..., ge=0.0, le=5.0)

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    id: int

    class Config:
        from_attributes = True

class SupplierListResponse(BaseModel):
    suppliers: List[SupplierResponse]

    class Config:
        from_attributes = True