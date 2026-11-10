from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional
import uuid

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.users import UserRoleTable
from uuid import UUID


# class UserRole(str, Enum):
#     admin = "admin"
#     sales_manager = "sales_manager"
#     warehouse_clerk = "warehouse_clerk"
#     purchasing_clerk = "purchasing_clerk"
#     accountant = "accountant"
#     director = "director"

class UserPermission(str, Enum):
    edit_order = "edit_order"
    edit_client = "edit_client"
    edit_good = "edit_good"
    edit_leftover = "edit_leftover"
    edit_finance = "edit_finance"
    edit_analitic = "edit_analitic"
    import_export_data = "import_export_data"


    

class UserResponse(BaseModel):
    id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
    phone: str
    photo: str
    role: str
    
    model_config = ConfigDict(from_attributes=True)

    @field_validator('role', mode='before')
    @classmethod
    def transform_role(cls, value):
        if isinstance(value, object):
            return str(value.name) if hasattr(value, 'name') else ''
        return ''

class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    phone: str
    photo: str
    created_at: datetime
    updated_at: datetime
    is_active: Optional[bool] = True
    role: str

class UpdateUserRoleRequest(BaseModel):
    id: UUID
    email: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    photo: Optional[str] = None
    role: str

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=1)


class CreateRoleRequest(BaseModel):
    name: str
    permissions: list[str] = [] 
    
class UpdateRoleRequest(BaseModel):
    name: str = ""
    permissions: list[str] = [] 
    

class CreatePermissionRequest(BaseModel):
    name: str

class UserRoleResponse(BaseModel):
    id: int
    name: str
    permissions: List[str]  # Ожидаем на выходе список строк

    # Включаем совместимость с ORM-моделями SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

    # Магия трансформации: превращаем объекты PermissionTable в строки
    @field_validator('permissions', mode='before')
    @classmethod
    def transform_permissions(cls, value):
        print('transform_permissions',[perm.name if hasattr(perm, 'name') else perm for perm in value])
        if isinstance(value, list):
            # Если внутри списка лежат объекты, берем у каждого поле .name
            return [perm.name if hasattr(perm, 'name') else perm for perm in value]
        return value