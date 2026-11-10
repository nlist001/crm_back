from fastapi import  APIRouter, HTTPException
from sqlalchemy import  delete, select
from sqlalchemy.orm import joinedload
from app.db import db_dependency
from app.stores.cell.schemas import CreateCellRequest,DeleteCellRequest, UpdateCellRequest
from app.models.stores import CellStocksTable, StoresTable, CellsTable
from app.models.products import ProductTable
from uuid import UUID

from app.stores.utils import getCellbyId, getStorebyId

router = APIRouter(
    prefix='/stores/cell',
    tags=["cell"]
)


@router.post("/")
async def create_cell(db: db_dependency, req: CreateCellRequest):
    getStorebyId(db, req.store_id)
    new_cell = CellsTable(**req.model_dump())
    db.add(new_cell)
    db.commit()
    db.refresh(new_cell)
    return new_cell

@router.put("/")
async def update_cell(db: db_dependency, req: UpdateCellRequest):
    cell = getCellbyId(db,req.store_id,req.cell_code)
    cell.is_active = req.is_active
    db.commit()
    db.refresh(cell)
    return cell

@router.delete("/")
async def del_cell(db: db_dependency, req: DeleteCellRequest):

    cell = getCellbyId(db,req.store_id,req.cell_code)

    stmt = delete(CellsTable).where(CellsTable.store_id == req.store_id, CellsTable.cell_code == req.cell_code)
    db.execute(stmt)
    db.commit()
    return cell

@router.get("/{store_id}")
async def get_cells(db: db_dependency, store_id:str):
     stmt = select(CellsTable).where(CellsTable.store_id == store_id)
     
     return db.scalars(stmt).all()