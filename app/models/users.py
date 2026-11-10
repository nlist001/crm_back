
import datetime
from typing import List
import uuid
import bcrypt
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from app.db import Base
from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, Table, UniqueConstraint, Uuid, String, Boolean, ARRAY, DateTime, func, select
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.orders import OrdersTable
    from app.models.stores import CellStocksReserveTable


class UserTable(Base):
    __tablename__='users'
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column( CheckConstraint("email LIKE '%_@_%._%'", name="chk_email_format"),unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(50))
    photo: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(default=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("user_role.id"))
    role: Mapped["UserRoleTable"] = relationship( back_populates="user")

    order: Mapped[List["OrdersTable"]] = relationship(back_populates="manager")
    cell_stocks_reserve: Mapped[List["CellStocksReserveTable"]] = relationship(back_populates="manager")

    @validates("password")
    def hash_password(self, password):
        if password:
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
        return password

    @classmethod
    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    @classmethod
    def get_users_query(self):
        return select(self).where(self.is_active)
        # return select(self).where(~self.is_active)


    __table_args__ = (
        # 1. Уникальное ограничение для пары колонок
        UniqueConstraint("username", "email", name="uq_user_username_email"),
        
        # 2. Ограничение CHECK
        # CheckConstraint("status IN ('active', 'banned')", name="check_user_status"),
        # CheckConstraint("name <> ''", name="check_name_notempty"),
        # CheckConstraint("name ~ '^[a-z0-9_-]+$'", name="check_name_format"), regular expression
        
        # 3. Индекс (если не создали через mapped_column)
        # Index("ix_user_email", "email"),
        
        # 4. Именованные параметры СУБД (передаются СЛОВАРЕМ в самом конце)
        # {
        #     "schema": "production",        # Название схемы в БД
        #     "comment": "Таблица пользователей", # Комментарий к таблице
        #     "postgresql_with_oids": False  # Специфичный параметр для PostgreSQL
        # }
    )
    

UserRolePermissionTable = Table(
    "user_role_permission",
    Base.metadata,
    Column("user_role_id", Integer, ForeignKey("user_role.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permission.id", ondelete="CASCADE"), primary_key=True),
)

class UserRoleTable(Base):
    __tablename__ = 'user_role'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    user: Mapped[List["UserTable"]] = relationship( back_populates="role")

    permissions: Mapped[list["PermissionTable"]] = relationship(
        secondary=UserRolePermissionTable, 
        back_populates="user_role"
    )



class PermissionTable(Base):
    __tablename__='permission'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    user_role: Mapped[list["UserRoleTable"]] = relationship(
        secondary=UserRolePermissionTable, 
        back_populates="permissions"
    )

