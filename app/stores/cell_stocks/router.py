from fastapi import  APIRouter
from sqlalchemy import  delete, select
from app.db import db_dependency
from app.models.stores import CellStocksTable

from app.stores.utils import getCellbyId, getProductById, getCellStockById
from app.stores.cell_stocks.schemas import UpdateProductInCellRequest, DeleteProductInCellRequest, GetProductInCellRequest

router = APIRouter(
    prefix='/stores/cell_stocks',
    tags=["cell stocks"]
)


@router.post("/")
async def add_product_to_cell(db: db_dependency, req: UpdateProductInCellRequest):
    getCellbyId(db,req.store_id,req.cell_code)
    getProductById(db,req.product_id)
    product_cell = CellStocksTable(**req.model_dump())
    db.add(product_cell)
    db.commit()
    db.refresh(product_cell)
    return product_cell

@router.put("/")
async def update_product_in_cell(db: db_dependency, req: UpdateProductInCellRequest):
    cell_stock = getCellStockById(db,req.id)
    
    for key, value in req.model_dump().items(): 
        setattr(cell_stock, key, value)
    db.commit()
    db.refresh(cell_stock)
    return cell_stock

@router.delete("/")
async def del_product_from_cell(db: db_dependency, req: DeleteProductInCellRequest):
    cell_stock = getCellStockById(db,req.id)
    
    stmt = delete(CellStocksTable).where(
        CellStocksTable.store_id == req.store_id,
        CellStocksTable.cell_code == req.cell_code
    )
    db.execute(stmt)
    db.commit()
    return cell_stock


@router.post("/get")
async def get_product_from_cell(db: db_dependency, req:GetProductInCellRequest):
    print('GetProductInCellRequest',req)
    return CellStocksTable.getProductFromCell(db,**req.model_dump())



