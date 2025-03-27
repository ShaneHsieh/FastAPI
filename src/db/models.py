from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

# Many-to-Many Relationship Table for Products and Suppliers
product_supplier = Table(
    "product_supplier", Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("supplier_id", Integer, ForeignKey("suppliers.id"))
)

# Product Model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    stock = Column(Integer, nullable=False, default=0)
    category = Column(String, nullable=True)
    discount = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    suppliers = relationship("Supplier", secondary=product_supplier, back_populates="products")
    history = relationship("ProductHistory", back_populates="product", cascade="all, delete-orphan")

# Supplier Model
class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_info = Column(String, nullable=True)
    rating = Column(Float, default=0.0)
    products = relationship("Product", secondary=product_supplier, back_populates="suppliers")

class ProductHistory(Base):
    __tablename__ = "product_histories"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="history")