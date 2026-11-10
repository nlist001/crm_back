from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models.stores import CellStocksTable, StoresTable, CellsTable
from app.models.products import ProductTable

def getStorebyId(db, id: str):
    store = db.get(StoresTable, id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store

def getCellbyId(db, store_id: str, cell_code: str):
    cell = db.get(CellsTable, (store_id, cell_code))
    if not cell:
        raise HTTPException(status_code=404, detail="Cell not found")
    return cell

def getProductById(db, id: str):
    product = db.get(ProductTable, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def getCellStockById(db, id: str):
    cell_stock = db.get(CellStocksTable, id)
    if not cell_stock:
        raise HTTPException(status_code=404, detail="Cell is empty")
    return cell_stock


