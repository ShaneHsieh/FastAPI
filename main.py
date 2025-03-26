from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.products import router as products_router
from src.api.v1.suppliers import router as suppliers_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router, prefix="/api/v1/products", tags=["products"])
app.include_router(suppliers_router, prefix="/api/v1/suppliers", tags=["suppliers"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Product API"}