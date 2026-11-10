from fastapi import  APIRouter
from sqlalchemy import  delete, select
from app.db import db_dependency
from app.stores.schemas import CreateStoreRequest, StoreResponse
from app.models.stores import StoresTable

from app.stores.utils import getStorebyId


router = APIRouter(
    prefix='/stores',
    tags=["stores"]
)

@router.get("/")
async def get_stores(db: db_dependency):
    stmt = select(StoresTable)
    return db.scalars(stmt).all()

@router.post("/")
async def create_store(db: db_dependency, req: CreateStoreRequest):
    new_store = StoresTable(**req.model_dump())
    db.add(new_store)
    db.commit()
    db.refresh(new_store)
    return new_store

@router.delete("/{id}")
async def del_store(db: db_dependency, id:str):
    store =  StoreResponse.model_validate(getStorebyId(db,id))
    stmt = delete(StoresTable).where( StoresTable.id == id )
    db.execute(stmt)
    db.commit()
    return store

@router.put("/{id}")
async def update_store(db: db_dependency, id:str, req: CreateStoreRequest):
    store = getStorebyId(db,id)
    for key, value in req.model_dump().items(): 
        setattr(store, key, value)
    db.commit()
    db.refresh(store)
    return store