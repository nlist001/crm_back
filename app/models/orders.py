

import datetime
from enum import Enum
from typing import List
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base
from sqlalchemy import Column, Index, ForeignKey, ForeignKeyConstraint, Integer, Table, Uuid, String, Boolean, DateTime, func

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.users import UserTable
    from app.models.partners import PartnersTable
    from app.models.products import ProductTable
    from app.models.stores import CellStocksReserveTable 

class OrdersTable(Base):
    __tablename__='orders'
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)

    manager_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    manager: Mapped["UserTable"] = relationship(back_populates="order")

    partner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("partners.id"))
    partner: Mapped["PartnersTable"] = relationship(back_populates="order")


    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    products_in_order: Mapped[list["ProductsInOrderTable"]] = relationship(back_populates="order")
    cell_stocks_reserve: Mapped[list["CellStocksReserveTable"]] = relationship(back_populates="order")


class ProductStatusInOrderTable(Base):
    __tablename__='product_status_in_order'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30))
    products_in_order: Mapped[list["ProductsInOrderTable"]] = relationship(back_populates="status")
    


# 2. Связующая таблица (Association Object) вместо обычного Table
class ProductsInOrderTable(Base):
    __tablename__ = "products_in_order"
    
    # Составной первичный ключ (Composite Primary Key) из внешних ключей
    order_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True)

    product_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)

    status_id: Mapped[int] = mapped_column(Integer, ForeignKey("product_status_in_order.id", ondelete="CASCADE"))

    count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    
    status: Mapped["ProductStatusInOrderTable"] = relationship(back_populates="products_in_order")
    product: Mapped["ProductTable"] = relationship(back_populates="products_in_order")
    order: Mapped["OrdersTable"] = relationship(back_populates="products_in_order")


