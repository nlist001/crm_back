from typing import List
from fastapi import  APIRouter, HTTPException
from sqlalchemy import Uuid, inspect, or_, select, update
from sqlalchemy.orm import joinedload, load_only, selectinload, session
from app.db import db_dependency
from app.products.schemas import CreateProductRequest, FilterProductRequest, ProductResponse
from app.models.products import ProductAdditionTable, ProductTable
from app.models.stores import CellStocksTable

router = APIRouter(
    prefix='/products',
    tags=["products"]
)


@router.post("/list", response_model=List[ProductResponse])
async def get_list(db: db_dependency, req: FilterProductRequest = None):
    stmt = select(ProductTable).filter(ProductTable.is_archive == False).options(joinedload(ProductTable.brand))
    stmt = stmt.options(joinedload(ProductTable.category))
    if req is not None:
        if req.store:
            stmt = stmt.join(CellStocksTable, CellStocksTable.product_id == ProductTable.id)\
            .where(CellStocksTable.store_id == req.store)
            print(stmt)
        if req.brand:
            stmt = stmt.filter(ProductTable.brand_id == req.brand)
        if req.category:
            stmt = stmt.filter(ProductTable.category_id == req.category)
        if req.search:
            stmt = stmt.filter(or_(
                ProductTable.name.like(f"%{req.search}%"), 
                ProductTable.sku.like(f"%{req.search}%"), 
                ProductTable.code.like(f"%{req.search}%")
            ))
        if req.sort:
            stmt = stmt.order_by(req.sort)
        if req.page:
            stmt = stmt.offset((req.page - 1) * req.page_size)
        if req.page_size:
            stmt = stmt.limit(req.page_size)
    products = db.scalars(stmt).all()
    return products


@router.post("/")
async def create_product(db: db_dependency, req: CreateProductRequest):
    print(type(req), req)
    product_fields = [c.key for c in inspect(ProductTable).mapper.column_attrs]
    new_product = ProductTable(**req.model_dump(include=product_fields))
    db.add(new_product)
    db.flush()

    new_product_addition = ProductAdditionTable(**req.model_dump(exclude=product_fields), product_id=new_product.id)
    
    db.add(new_product_addition)
    db.commit()

      # new_product = ProductTable(**req.model_dump(include=product_fields))
    # new_product_addition = ProductAdditionTable(**req.model_dump(exclude=product_fields), product=new_product)
    # db.add(new_product)
    # db.add(new_product_addition)
    # db.commit()
    # 
  
   

@router.put("/{id}")
async def update_product(db: db_dependency, req: CreateProductRequest):
    print('update_users',req)
   
    pass


@router.delete("/", response_model=ProductResponse)
async def del_product(db: db_dependency, id:str):
    product = db.query(ProductTable).filter(ProductTable.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.is_archive = True
    db.commit()
    return product



@router.get("/{id}")
async def get_product(db: db_dependency, id: str):
    stmt = select(ProductTable).where(ProductTable.id == id).options(joinedload(ProductTable.addition))
    product = db.scalars(stmt).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # product_dict = ProductResponse.model_validate(product).model_dump()
    # print(product_dict)
    return product
    # ProductResponse.model_validate(product)