
from fastapi import  APIRouter, HTTPException
from sqlalchemy import Uuid, select, update

from app.db import db_dependency

from app.products.schemas import CreateBrandsRequest
from app.models.products import BrandTable
router = APIRouter(
    tags=["brands"],
)


@router.get("/brands")
async def get_list(db: db_dependency):
    stmt = select(BrandTable)
    return db.scalars(stmt).all()


@router.post("/brands")
async def create(db: db_dependency, req: CreateBrandsRequest):
    new_brands= BrandTable(**req.model_dump())
    db.add(new_brands)
    db.commit()
    db.refresh(new_brands)
    return new_brands

@router.delete("/brands")
async def del_brands(db: db_dependency, id:str):
    brands = db.query(BrandTable).filter(BrandTable.id == id).first()
    if not brands:
        raise HTTPException(status_code=404, detail="brands not found")
    db.delete(brands)
    db.commit()
    return brands
