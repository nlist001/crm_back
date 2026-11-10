from typing import Annotated
from fastapi import  APIRouter, Depends, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from auth.auth import create_access_token, credentials_exception, current_user_dependency


from auth.schemas import UserTable, UserRole
from db import db_dependency
from todo.schemas import TodoTable


router = APIRouter(
    prefix='/admin',
    tags=["admin"]
)

@router.get("/todos")
async def get_todos(current_user: current_user_dependency, db: db_dependency):
    if current_user.role != UserRole.ADMIN:
        raise credentials_exception
    return db.query(TodoTable).all()