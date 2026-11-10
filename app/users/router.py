from os import name
from typing import List, Set
from uuid import UUID
from fastapi import  APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from sqlalchemy import Uuid, select, update
from sqlalchemy.orm import load_only, selectinload, session
from app.auth.auth import current_user_dependency, pwd_context

from app.db import db_dependency
from app.users.schemas import  UpdateUserRoleRequest, UserResponse
from app.models.users import PermissionTable, UserTable, UserRoleTable

# np = PermissionTable()
# urt = UserRoleTable()
# urt.permissions.append(np)
# session.add_all([urt,np])
# session.commit()

router = APIRouter(
    prefix='/users',
    tags=["users"]
)

@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: current_user_dependency):
    return current_user


@router.get("/", response_model=List[UserResponse])
async def get_users(db: db_dependency):
    stmt = select(UserTable).options(selectinload(UserTable.role))
    return db.scalars(stmt).all()
    #return db.query(UserTable).all()

@router.put("/")
async def update_users(db: db_dependency, req: List[UpdateUserRoleRequest]):
    print('update_users',req)
    # roles_stmt = select(UserRoleTable);
    # roles = db.scalars(roles_stmt).all()
    # users_ids = [item.id for item in req]
    # users_role = [item.role for item in req]
    for item in req:
        user_stmt = select(UserTable)\
            .where(UserTable.id == item.id)\
            .options(selectinload(UserTable.role))\
            .where(UserTable.role.has(UserRoleTable.name != item.role))
        user = db.scalars(user_stmt).one();
        if user:
            role = db.scalars(select(UserRoleTable).where(UserRoleTable.name == item.role)).one();
            if role:
                print('before user',user.role.__dict__)

                user.role = role;
                print('item',item)
                print('user',user.role.__dict__)
                db.commit()
            
        
        
        # user.role_id = 
        # db.commit()
        #  and UserTable.role.has(UserRoleTable.name.in_(users_role)))
    # users = db.scalars([user_stmt]).all()


    
    pass


@router.delete("/", response_model=UserResponse)
async def del_user(db: db_dependency, id:str):
    user = db.query(UserTable).filter(UserTable.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.query(UserTable).filter(UserTable.id == id).delete()
    db.commit()
    return user



@router.get("/{id}", response_model=UserResponse)
async def get_user(db: db_dependency, id: str):
    # stmt = select(UserTable).join(UserRoleTable, UserTable.role_id == UserRoleTable.id).where(UserTable.id == id)
    stmt = select(UserTable).where(UserTable.id == id).options(selectinload(UserTable.role))
    print(stmt)
    user = db.scalars(stmt).first()
    print('user',user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user