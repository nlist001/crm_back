from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pickletools import int4
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from uuid import UUID

class CreateCellRequest(BaseModel):
    store_id: str = Field(max_length=50)
    cell_code: str = Field(max_length=50)
    is_active: bool = Field(default=True)

class UpdateCellRequest(BaseModel):
    store_id: str = Field(max_length=50)
    cell_code: str = Field(max_length=50)
    is_active: bool = Field(default=True)

class DeleteCellRequest(BaseModel):
    store_id: str = Field(max_length=50)
    cell_code: str = Field(max_length=50)
