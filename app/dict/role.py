from typing import List, Set
from uuid import UUID
from fastapi import  APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from sqlalchemy import Uuid, select, update
from sqlalchemy.orm import load_only, selectinload, session
from app.auth.auth import current_user_dependency, pre_hash, pwd_context

from app.db import db_dependency
from app.models.users import PermissionTable, UserTable, UserRoleTable, UserRolePermissionTable
from app.users.schemas import CreatePermissionRequest, CreateRoleRequest, UpdateRoleRequest, UserResponse, UserRoleResponse, UserVerification

router = APIRouter(
    tags=["roles"]
)

async def update_permission( db: db_dependency,  req: UpdateRoleRequest, role_permissions: list[PermissionTable]=[]):
    print('update_permission')
    if len(req.permissions) > 0:
        permissions = db.query(PermissionTable).all()
        all_permissions = set(map(lambda p: p.name,permissions))
        set_role_permissions = set(req.permissions)
        to_remove = set_role_permissions - all_permissions
        print('to_remove',to_remove)

        if len(to_remove) > 0:
            set_role_permissions: Set[str] = set_role_permissions - to_remove

        return role_permissions +  [p for p in permissions if p.name in set_role_permissions]
    return role_permissions




@router.get("/roles", response_model=List[UserRoleResponse])
async def get_roles( db: db_dependency):
    print("/roles")
    #roles = db.query(UserRoleTable).all()
    stmt = select(UserRoleTable).options(selectinload(UserRoleTable.permissions))
    return db.scalars(stmt).all()


@router.post("/role")
async def create_role( db: db_dependency, req: CreateRoleRequest):
    role = db.query(UserRoleTable).filter(UserRoleTable.name == req.name).first()
    if role:
        raise HTTPException(status_code=401, detail="Role "+req.name+" is already exist")
    new_role = UserRoleTable(name=req.name)
    new_role.permissions = await update_permission(db=db,req=req)

   
    db.add(new_role)
    db.commit()

@router.put("/role/{id}")
async def update_role( db: db_dependency, id: int, req: UpdateRoleRequest):
    if req.name =="" and len(req.permissions) == 0:
        raise HTTPException(status_code=401, detail="You must fill at least one field "+req.model_dump())
        
    role = db.query(UserRoleTable).filter(UserRoleTable.id == id).first()
    if not role:
        raise HTTPException(status_code=401, detail="Role not found")


    # if req.name and len(req.permissions) == 0:
    #     new_role_name = db.query(UserRoleTable).filter(UserRoleTable.name == req.name).first()
    #     if new_role_name:
    #         raise HTTPException(status_code=401, detail="Role "+req.name+" is already exist 1")
        
        role.name = req.name
        
    role.permissions = await update_permission(db=db,req=req,role_permissions=role.permissions)

    
    db.commit()
    db.refresh(role)
    print('role',role.__dict__)
    return role

