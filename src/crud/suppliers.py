from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..db.models import Supplier
from ..schemas.suppliers import SupplierCreate, SupplierResponse

def create_supplier(db: Session, supplier: SupplierCreate) -> SupplierResponse:
    db_supplier = Supplier(**supplier.dict())
    db.add(db_supplier)
    try:
        db.commit()
        db.refresh(db_supplier)
    except IntegrityError:
        db.rollback()
        raise ValueError("Supplier with this name already exists.")
    return SupplierResponse.from_orm(db_supplier)

def get_supplier(db: Session, supplier_id: int) -> SupplierResponse:
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if supplier is None:
        raise ValueError("Supplier not found.")
    return SupplierResponse.from_orm(supplier)

def get_suppliers(db: Session, skip: int = 0, limit: int = 10) -> list[SupplierResponse]:
    suppliers = db.query(Supplier).offset(skip).limit(limit).all()
    return [SupplierResponse.from_orm(supplier) for supplier in suppliers]

def update_supplier(db: Session, supplier_id: int, supplier: SupplierCreate) -> SupplierResponse:
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if db_supplier is None:
        raise ValueError("Supplier not found.")
    for key, value in supplier.dict().items():
        setattr(db_supplier, key, value)
    db.commit()
    db.refresh(db_supplier)
    return SupplierResponse.from_orm(db_supplier)

def delete_supplier(db: Session, supplier_id: int) -> None:
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if db_supplier is None:
        raise ValueError("Supplier not found.")
    db.delete(db_supplier)
    db.commit()