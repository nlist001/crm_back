
from fastapi import  APIRouter, HTTPException
from app.db import db_dependency
from app.models.users import PermissionTable
from app.users.schemas import CreatePermissionRequest
router = APIRouter(
    tags=["permissions"]
)

@router.post("/permission")
async def create_permission( db: db_dependency, req: CreatePermissionRequest):
    permission = db.query(PermissionTable).filter(PermissionTable.name == req.name).first()
    if permission:
        raise HTTPException(status_code=401, detail="Permission "+req.name+" is already exist")
    new_permission = PermissionTable(**req.model_dump())
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return new_permission

@router.get("/permissions")
async def get_permissions( db: db_dependency):
    permissions = db.query(PermissionTable).all()
    return permissions

