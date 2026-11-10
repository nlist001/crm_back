from pydantic import BaseModel, Field
from uuid import UUID


class UpdateProductInCellRequest(BaseModel):
    store_id: str = Field(max_length=50)
    cell_code: str = Field(max_length=50)
    product_id: UUID
    count: int = Field(default=0)
    min_count: int = Field(default=0)

class DeleteProductInCellRequest(BaseModel):
    store_id: str = Field(max_length=50)
    cell_code: str = Field(max_length=50)

class GetProductInCellRequest(BaseModel):
    store_id: str = Field(max_length=50)
    cell_code: str = Field(max_length=50)
    withProductInfo: bool = Field(default=False)
    
    
