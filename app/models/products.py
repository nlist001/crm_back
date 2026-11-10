
import datetime
from enum import Enum
from typing import List
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base
from sqlalchemy import UUID, Column, DOUBLE_PRECISION, ForeignKey, Integer, Numeric, Table, Uuid, String, Boolean, ARRAY, DateTime, func
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.orders import ProductsInOrderTable
    from app.models.stores import CellStocksReserveTable




class BrandTable(Base):
    __tablename__='brands'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150))
    products: Mapped[list["ProductTable"]] = relationship(back_populates="brand")


class CategoryTable(Base):
    __tablename__='category'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150))
    products: Mapped[list["ProductTable"]] = relationship(back_populates="category")



class ProductTable(Base):
    __tablename__='products'
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(150))
    photo: Mapped[str] = mapped_column(String)
    sku: Mapped[str] = mapped_column(String)
    code: Mapped[str] = mapped_column(String)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
    brand: Mapped["BrandTable"] = relationship(back_populates="products")
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["CategoryTable"] = relationship(back_populates="products")
    price: Mapped[float] = mapped_column(Numeric)
    # margin  = Column(Numeric)
    is_archive: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
 

    addition = relationship("ProductAdditionTable", 
        back_populates="product", 
        uselist=False, 
        cascade="all, delete-orphan",
        single_parent=True,
        passive_deletes=True
    )

    store_cell_stocks = relationship("CellStocksTable", back_populates="product", cascade="all, delete-orphan")
    
    products_in_order: Mapped[list["ProductsInOrderTable"]] = relationship(back_populates="product")
    cell_stocks_reserve: Mapped[list["CellStocksReserveTable"]] = relationship(back_populates="product")


class ProductAdditionTable(Base):
    __tablename__='products_addition'
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    description: Mapped[str] = mapped_column(String(500))
    producer: Mapped[str] = mapped_column(String(150))
    jan: Mapped[str] = mapped_column(String)
    isbn: Mapped[str] = mapped_column(String)
    mpn: Mapped[str] = mapped_column(String)
    external_code: Mapped[str] = mapped_column(String)
    unit: Mapped[str] = mapped_column(String)   
    weight: Mapped[str] = mapped_column(String)
    length: Mapped[int] = mapped_column(Integer)
    width: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    photos: Mapped[str] = mapped_column(String)
    retail_price: Mapped[float] = mapped_column(Numeric)
    wholesale_price: Mapped[float] = mapped_column(Numeric)
    nds: Mapped[int] = mapped_column(Integer)
    packing_type: Mapped[str] = mapped_column(String)
    inventory_method: Mapped[str] = mapped_column(String)
    product_type: Mapped[str] = mapped_column(String)
    rop: Mapped[str] = mapped_column(String)
    upc_1: Mapped[str] = mapped_column(String)
    upc_2: Mapped[str] = mapped_column(String)
    ozon_link: Mapped[str] = mapped_column(String)

    product_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey('products.id'), nullable=False, index=True, unique=True)
    product = relationship("ProductTable", back_populates="addition",passive_deletes=True)


    
    # role_id: Mapped[Integer] = mapped_column(ForeignKey("user_role.id"))
    # role: Mapped["UserRoleTable"] = relationship( back_populates="user")
    