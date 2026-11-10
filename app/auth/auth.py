from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import Uuid
from app.models.users import UserTable
from app.config import settings
from typing import Annotated
import hashlib
import logging

log = logging.getLogger("uvicorn")

import jwt
from jwt.exceptions import InvalidTokenError

from app.db import db_dependency
# Секретные ключи обычно хранят в .env


# Указывает FastAPI, где искать токен (в заголовке Authorization: Bearer <token>)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# Создаем контекст и указываем схему хеширования (рекомендуется bcrypt или argon2)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def pre_hash(password:str): 
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


# Функция проверки токена (Зависимость)
async def get_current_user(db: db_dependency, token: str = Depends(oauth2_scheme)):
    try:
        # Декодируем JWT-токен
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")

        if not username:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
        
    user = db.query(UserTable).filter(UserTable.username == username).first()

    if user is None:
        raise credentials_exception

    return user

async def create_access_token(username:str, user_id: str, role:str, expire_delta: timedelta = timedelta(minutes=20)):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expire_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,settings.SECRET_KEY, algorithm=settings.ALGORITHM)


current_user_dependency = Annotated[UserTable, Depends(get_current_user)]