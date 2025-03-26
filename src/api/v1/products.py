from fastapi import APIRouter, Depends, HTTPException ,status
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.crud.products import create_product, get_product, get_products, update_product, delete_product
from src.schemas.products import ProductCreate, ProductResponse

router = APIRouter()

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
def update_existing_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = update_product(db=db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}", status_code=204)
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    result = delete_product(db=db, product_id=product_id)
    if result:
        raise HTTPException(status_code=404, detail="Product not found")
    return 

@router.get("/search/")
def search_products(name: str = None, category: str = None, db: Session = Depends(get_db)):
    products = get_products(db=db, name=name, category=category)
    return products