from pydantic import BaseModel, ConfigDict, Field, field_validator
    
class CreateStoreRequest(BaseModel):
    id: str = Field(max_length=50)
    name: str = Field(max_length=150)
    address: str = Field(max_length=500)
    is_active: bool = Field(default=True)

class StoreResponse(BaseModel):
    id: str
    name: str 
    address: str 
    is_active: bool

    model_config = ConfigDict(from_attributes=True) 


