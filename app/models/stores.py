

import datetime
from enum import Enum
from typing import List
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship
from app.db import Base
from sqlalchemy import Index, ForeignKey, ForeignKeyConstraint, Integer, Uuid, String, Boolean, DateTime,select, event, func
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.products import ProductTable
    from app.models.users import UserTable
    from app.models.orders import OrdersTable




class StoresTable(Base):
    __tablename__='stores'
    id: Mapped[str] = mapped_column(String(50), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150))
    address: Mapped[str] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean,default=True)


class CellsTable(Base):
    __tablename__='store_cells'
    store_id: Mapped[str] = mapped_column(ForeignKey("stores.id"), primary_key=True)
    cell_code: Mapped[str] = mapped_column(String(50), primary_key=True, index=True )
    stocks: Mapped[list["CellStocksTable"]] = relationship(back_populates="cell")
    
    is_active: Mapped[bool] = mapped_column(Boolean,default=True)
    


class CellStocksTable(Base):
    __tablename__='cell_stocks'
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    count: Mapped[int] = mapped_column(Integer, default=0)
    min_count: Mapped[int] = mapped_column(Integer, default=0)

    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"))
    product: Mapped["ProductTable"] = relationship(back_populates="store_cell_stocks")

    # Колонки для составного внешнего ключа на ячейку
    store_id: Mapped[str] = mapped_column(String(50))
    cell_code: Mapped[str] = mapped_column(String(50))
    
    # Явное объединение колонок в составной внешний ключ
    __table_args__ = (
        ForeignKeyConstraint(
            ["store_id", "cell_code"],
            ["store_cells.store_id", "store_cells.cell_code"]
        ),
        Index("ix_cell_stocks_store_cell", "store_id", "cell_code"),
        Index("ix_cell_stocks_product_store_cell", "product_id", "store_id", "cell_code", unique=True),
    )
    
    # Опционально: объектная связь (relationship) для удобной работы в коде
    cell: Mapped["CellsTable"] = relationship(back_populates="stocks")

    @classmethod
    def getProductFromCell(self, db, store_id: str, cell_code: str, withProductInfo: bool = False):
        stmt = select(self).where(
            self.store_id == store_id, 
            self.cell_code == cell_code
        )
        if withProductInfo:
            stmt = stmt.options(joinedload(self.product))
        cell_stock = db.scalars(stmt).first()
        
        if not cell_stock:
            raise HTTPException(status_code=404, detail="Product not found")
        return cell_stock


class CellStocksReserveTable(Base):
    __tablename__='cell_stocks_reserve'
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)

    # Колонки для составного внешнего ключа на ячейку
    store_id: Mapped[str] = mapped_column(String(50))
    cell_code: Mapped[str] = mapped_column(String(50))

    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.id"))
    product: Mapped["ProductTable"] = relationship(back_populates="cell_stocks_reserve")


    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id"), nullable=True)
    order: Mapped["OrdersTable"] = relationship(back_populates="cell_stocks_reserve")

    manager_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    manager: Mapped["UserTable"] = relationship(back_populates="cell_stocks_reserve")


    count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    contact_fio_company: Mapped[str] = mapped_column(String(200))
    phone: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(100))
    comment: Mapped[str] = mapped_column(String(500))

    
    # Явное объединение колонок в составной внешний ключ
    __table_args__ = (
        ForeignKeyConstraint(
            ["store_id", "cell_code"],
            ["store_cells.store_id", "store_cells.cell_code"]
        ),
        # Index("ix_cell_stocks_store_cell", "store_id", "cell_code"),
        # Index("ix_cell_stocks_product_store_cell", "product_id", "store_id", "cell_code", unique=True),
    )

    

# @event.listens_for("CellStocksReserveTable","before_insert")
@event.listens_for(CellStocksReserveTable,"before_update")
def testexample(mapper, connection, target):
    if target.count < 0:
        target.count = 0
   
