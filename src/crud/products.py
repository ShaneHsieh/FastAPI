from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from ..db.models import Product, Supplier
from ..schemas.products import ProductCreate, ProductResponse
from ..db.models import ProductHistory
from datetime import datetime

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

def record_product_history(db: Session, product_id: int, price: float, stock: int):
    history = ProductHistory(product_id=product_id, price=price, stock=stock)
    db.add(history)
    db.commit()

def update_product(db: Session, product_id: int, product_data: ProductCreate) -> Optional[ProductResponse]:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        if "price" in product_data.dict(exclude_unset=True) and db_product.price != product_data.price:
            record_product_history(db, product_id, product_data.price, db_product.stock)
        if "stock" in product_data.dict(exclude_unset=True) and db_product.stock != product_data.stock:
            record_product_history(db, product_id, db_product.price, product_data.stock)
        for key, value in product_data.dict(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return db_product
    return None

def delete_product(db: Session, product_id: int) -> Optional[ProductResponse]:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return db_product
    return None

def get_product_history(db: Session, product_id: int, start_time: datetime, end_time: datetime) -> List[ProductHistory]:
    return db.query(ProductHistory).filter(
        ProductHistory.product_id == product_id,
        ProductHistory.timestamp >= start_time,
        ProductHistory.timestamp <= end_time
    ).all()

def search_products(
    db: Session,
    name: Optional[str] = None,
    description: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_stock: Optional[int] = None,
    max_stock: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    sort_by: Optional[str] = None,
    sort_order: str = "asc"
) -> List[ProductResponse]:
    query = db.query(Product)

    # 模糊查詢
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))
    if description:
        query = query.filter(Product.description.ilike(f"%{description}%"))

    # 條件篩選
    if category:
        query = query.filter(Product.category == category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if min_stock is not None:
        query = query.filter(Product.stock >= min_stock)
    if max_stock is not None:
        query = query.filter(Product.stock <= max_stock)

    # 排序
    if sort_by:
        sort_column = getattr(Product, sort_by, None)
        if sort_column is not None:
            query = query.order_by(sort_column.desc() if sort_order == "desc" else sort_column.asc())

    # 分頁
    query = query.offset(skip).limit(limit)

    return query.all()