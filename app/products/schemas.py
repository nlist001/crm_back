
from datetime import datetime
from enum import Enum
from pickletools import int4
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from uuid import UUID

    
class CreateProductRequest(BaseModel):
    name: str
    photo: str
    sku: str
    code: str
    brand_id: int
    category_id: int
    price: int
    # margin:int

    description: str = Field(max_length=500)
    producer: str = Field(max_length=150)
    jan: str
    isbn: str
    mpn: str
    external_code: str
    unit: str
    weight: str
    length: int
    width: int
    height: int
    photos: str
    created_at: datetime
    updated_at: datetime
    retail_price: float
    wholesale_price: float
    nds: int
    
    packing_type: str
    inventory_method: str
    product_type: str
    rop: str
    upc_1: str
    upc_2: str
    ozon_link: str

def transform_fields(value):
        if isinstance(value, object):
            return str(value.name) if hasattr(value, 'name') else ''
        return ''
        
class ProductResponse(BaseModel):

    id: UUID
    name: str
    photo: str
    sku: str
    code: str
    brand: str
    category : str
    price: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator('category', mode='before')
    @classmethod
    def transform_category(cls, value):
        return transform_fields(value)

    @field_validator('brand', mode='before')
    @classmethod
    def transform_brand(cls, value):
        return transform_fields(value)

class FilterProductRequest(BaseModel):
   store: str | None = None
   brand: int | None = None
   category: int | None = None
   search: str | None = None
   sort: str | None = None
   page: int | None = None
   page_size: int | None = None

class CreateCategoryRequest(BaseModel):
    name: str = Field(max_length=150)


class CreateBrandsRequest(BaseModel):
    name: str = Field(max_length=150)

