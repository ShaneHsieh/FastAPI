from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from ..db.models import Product, Supplier
from ..schemas.products import ProductCreate, ProductResponse

def create_product(db: Session, product: ProductCreate) -> ProductResponse:
    db_product = Product(
        name=product.name,
        price=product.price,
        description=product.description,
        stock=product.stock,
        category=product.category,
        discount=product.discount,
        suppliers = db.query(Supplier).filter(Supplier.id.in_(product.supplier_ids)).all(),
    )
    
    db.add(db_product)
    try:
        db.commit()
        db.refresh(db_product)
    except IntegrityError:
        db.rollback()
        raise ValueError("Product creation failed due to integrity error.")
    return db_product

def get_product(db: Session, product_id: int) -> Optional[ProductResponse]:
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10) -> List[ProductResponse]:
    return db.query(Product).offset(skip).limit(limit).all()

def update_product(db: Session, product_id: int, product_data: ProductCreate) -> Optional[ProductResponse]:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        for key, value in product_data.dict(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return db_product
    return None

def delete_product(db: Session, product_id: int) -> Optional[ProductResponse]:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise ValueError("Product not found")
    db.delete(db_product)
    db.commit()
    return db_product