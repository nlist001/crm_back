

import datetime
from enum import Enum
from typing import List
import uuid 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base
from sqlalchemy import Index, ForeignKey, ForeignKeyConstraint, Integer, Uuid, String, Boolean, DateTime, func
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.users import UserTable
    from app.models.orders import OrdersTable


class PartnersTypeTable(Base):
    __tablename__='partners_type'
    id: Mapped[int] = mapped_column(Uuid, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))

    partner: Mapped[List["PartnersTable"]] = relationship( back_populates="type")

class PartnersRoleTable(Base):
    __tablename__='partners_role'
    id: Mapped[int] = mapped_column(Uuid, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))

    partner: Mapped[List["PartnersTable"]] = relationship( back_populates="role")



class PartnersTable(Base):
    __tablename__='partners'
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(50))

    type_id: Mapped[int] = mapped_column(ForeignKey("partners_type.id"))
    type: Mapped["PartnersTypeTable"] = relationship(back_populates="partner")

    role_id: Mapped[int] = mapped_column(ForeignKey("partners_role.id"))
    role: Mapped["PartnersRoleTable"] = relationship(back_populates="partner")

    parent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("partners.id"), nullable=True)


    name: Mapped[str] = mapped_column(String(200))
    surename: Mapped[str] = mapped_column(String(200))
    midname: Mapped[str] = mapped_column(String(200))
    phone: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(100))


    addition: Mapped["PartnersAdditionTable"] = relationship(
        back_populates="parent",
        uselist=False, 
        cascade="all, delete-orphan",
        passive_deletes=True,
        single_parent=True
    )

    order: Mapped[List["OrdersTable"]] = relationship(back_populates="partner")


class PartnersAdditionTable(Base):
    __tablename__='partners_addition'
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    country: Mapped[str] = mapped_column(String(200))
    address: Mapped[str] = mapped_column(String(200))

    is_vip: Mapped[bool] = mapped_column(Boolean, default=False)
    inn: Mapped[str] = mapped_column(String(12))
    kpp: Mapped[str] = mapped_column(String(9), nullable=True)
    ogrn: Mapped[str] = mapped_column(String(15))

    ras_account: Mapped[str] = mapped_column(String(20))
    corr_account: Mapped[str] = mapped_column(String(20))
    bik: Mapped[str] = mapped_column(String(9))
    bank: Mapped[str] = mapped_column(String(200))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    parent_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey('partners.id',ondelete="CASCADE"), nullable=False, unique=True)
    parent = relationship("PartnersTable", back_populates="addition",passive_deletes=True)






