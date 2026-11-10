
from fastapi import  APIRouter, HTTPException
from sqlalchemy import Uuid, select, update
from app.db import db_dependency
from app.products.schemas import CreateCategoryRequest
from app.models.products import CategoryTable

router = APIRouter(
    tags=["category"]
)


@router.get("/category")
async def get_list(db: db_dependency):
    stmt = select(CategoryTable)
    return db.scalars(stmt).all()


@router.post("/category")
async def create(db: db_dependency, req: CreateCategoryRequest):
    new_category= CategoryTable(**req.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.delete("/category")
async def del_category(db: db_dependency, id:str):
    category = db.query(CategoryTable).filter(CategoryTable.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.delete()
   
    return category
