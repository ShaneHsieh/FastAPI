from fastapi import APIRouter, Depends, HTTPException , status
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.crud.suppliers import create_supplier, get_supplier, get_suppliers, update_supplier, delete_supplier
from src.schemas.suppliers import SupplierCreate, SupplierResponse
from typing import List
from src.schemas.suppliers import SupplierUpdate  # 假設 SupplierUpdate 是用於更新的 schema

router = APIRouter()

@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_new_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    return create_supplier(db=db, supplier=supplier)

@router.get("/{supplier_id}", response_model=SupplierResponse)
def read_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = get_supplier(db=db, supplier_id=supplier_id)
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.get("/", response_model=list[SupplierResponse])
def read_suppliers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    suppliers = get_suppliers(db=db, skip=skip, limit=limit)
    return suppliers

@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_existing_supplier(supplier_id: int, supplier: SupplierCreate, db: Session = Depends(get_db)):
    updated_supplier = update_supplier(db=db, supplier_id=supplier_id, supplier=supplier)
    if updated_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return updated_supplier

@router.delete("/{supplier_id}", status_code=204)
def delete_existing_supplier(supplier_id: int, db: Session = Depends(get_db)):
    try:
        delete_supplier(db=db, supplier_id=supplier_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return

@router.post("/batch", response_model=List[SupplierResponse], status_code=status.HTTP_201_CREATED)
def create_suppliers_batch(suppliers: List[SupplierCreate], db: Session = Depends(get_db)):
    created_suppliers = [create_supplier(db=db, supplier=supplier) for supplier in suppliers]
    return created_suppliers

@router.put("/batch", response_model=List[SupplierResponse])
def update_suppliers_batch(suppliers: List[SupplierUpdate], db: Session = Depends(get_db)):
    updated_suppliers = []
    for supplier in suppliers:
        updated_supplier = update_supplier(db=db, supplier_id=supplier.id, supplier=supplier)
        if updated_supplier is None:
            raise HTTPException(status_code=404, detail=f"Supplier with ID {supplier.id} not found")
        updated_suppliers.append(updated_supplier)
    return updated_suppliers

@router.delete("/batch", status_code=204)
def delete_suppliers_batch(supplier_ids: List[int], db: Session = Depends(get_db)):
    for supplier_id in supplier_ids:
        result = delete_supplier(db=db, supplier_id=supplier_id)
        if result:
            raise HTTPException(status_code=404, detail=f"Supplier with ID {supplier_id} not found")
    return