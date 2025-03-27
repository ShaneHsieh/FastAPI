from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.crud.products import create_product, get_product, get_products, update_product, delete_product , get_product_history, search_products
from src.schemas.products import ProductCreate, ProductResponse
from typing import List, Optional
from src.schemas.products import ProductUpdate  # 假設有 ProductUpdate schema
from datetime import datetime
from src.schemas.products import ProductHistoryResponse

router = APIRouter()

@router.post("/batch", response_model=List[ProductResponse], status_code=status.HTTP_201_CREATED)
def create_multiple_products(products: List[ProductCreate], db: Session = Depends(get_db)):
    created_products = [create_product(db=db, product=product) for product in products]
    return created_products

@router.put("/batch", response_model=List[ProductResponse])
def update_multiple_products(products: List[ProductUpdate], db: Session = Depends(get_db)):
    updated_products = []
    for product in products:
        result = update_product(db=db, product_id=product.id, product_data=product)
        if result is None:
            raise HTTPException(status_code=404, detail=f"Product with ID {product.id} not found")
        updated_products.append(result)
    return updated_products

@router.delete("/batch", status_code=204)
def delete_multiple_products(ids: str , db: Session = Depends(get_db)):
    product_ids = [int(id) for id in ids.split(",")]
    deleted_fail_products = []
    for product_id in product_ids:
        result = delete_product(db=db, product_id=product_id)
        if result is None:
            deleted_fail_products.append(product_id)
    if deleted_fail_products:
        raise HTTPException(status_code=404, detail=f"Products with ID {deleted_fail_products} not found")
    return

@router.get("/advanced-search", response_model=List[ProductResponse])
def advanced_search_products(
    name: Optional[str] = None,
    description: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_stock: Optional[int] = None,
    max_stock: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    sort_by: Optional[str] = Query(None, regex="^(name|price|stock|created_at|updated_at)$"),
    sort_order: str = Query("asc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    products = search_products(
        db=db,
        name=name,
        description=description,
        category=category,
        min_price=min_price,
        max_price=max_price,
        min_stock=min_stock,
        max_stock=max_stock,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return products

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = create_product(db=db, product=product)
    return new_product

@router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.get("/", response_model=list[ProductResponse])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = get_products(db=db, skip=skip, limit=limit)
    return products

@router.put("/{product_id}", response_model=ProductResponse)
def update_existing_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = update_product(db=db, product_id=product_id, product_data=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}", status_code=204)
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    result = delete_product(db=db, product_id=product_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return 

@router.get("/{product_id}/history", response_model=List[ProductHistoryResponse])
def read_product_history(
    product_id: int,
    start_time: datetime,
    end_time: datetime,
    db: Session = Depends(get_db)
):
    history = get_product_history(db, product_id, start_time, end_time)
    if not history:
        raise HTTPException(status_code=404, detail="No history found for the given product and time range")
    return history