from typing import Annotated
from fastapi import  APIRouter, Depends, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from app.models.users import UserTable, UserRoleTable
from app.users.schemas import CreateUserRequest
from app.auth.auth import create_access_token, pre_hash, pwd_context
from fastapi.security import OAuth2PasswordRequestForm
from app.db import db_dependency
from app.auth.auth import current_user_dependency, pre_hash, pwd_context
from app.users.schemas import UserVerification


router = APIRouter(
    #prefix='/auth',
    tags=["auth"]
)



@router.post("/signup")
async def create_user( db: db_dependency, req: CreateUserRequest):
    roles = db.query(UserRoleTable)
    role = roles.filter(UserRoleTable.name == req.role).first()
    role_list = ", ".join(map(lambda user_role: user_role.name,roles.all()))

    if not role:
       raise HTTPException(status_code=404, detail="User role not found. Role should be one of "+role_list) 

    # hashed_password = await run_in_threadpool(pwd_context.hash, pre_hash(req.password))
    # new_user = UserTable(**req.model_dump(exclude={"password","role"}), password=hashed_password, role=role)
    new_user = UserTable(**req.model_dump(role=role))
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/password")
async def change_password( current_user: current_user_dependency, db: db_dependency, user_verification:UserVerification):
 
    
    # if not pwd_context.verify(pre_hash(user_verification.password),current_user.password):
    if not current_user.check_password(user_verification.password):
        raise HTTPException(status_code=401, detail="Error on password change")

    # current_user.password = await run_in_threadpool(pwd_context.hash, pre_hash(user_verification.new_password))
    current_user.password = user_verification.new_password

    db.add(current_user)
    db.commit()

    return current_user


@router.post("/token")#, response_model= UserResponce)
async def login( db: db_dependency, req: Annotated[OAuth2PasswordRequestForm, Depends()]):

    user = db.query(UserTable).filter(UserTable.username == req.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    if not pwd_context.verify(pre_hash(req.password), user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = await create_access_token(user.username,str(user.id),user.role.name)
    return {
        "access_token": token, 
        "token_type": "bearer"
    }
