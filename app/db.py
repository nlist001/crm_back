from typing import Annotated
from contextlib import asynccontextmanager, contextmanager
from fastapi import Depends

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker,DeclarativeBase
from app.config import settings

class Base(DeclarativeBase):
    pass

import app.models.users
import app.models.partners 
import app.models.products 
import app.models.stores
import app.models.orders

# diagram = erd.create(metadata)
# diagram.draw("database_schema.png")
# print("Diagram drawn successfully without system Graphviz dependency!")

#engine = create_engine(settings.DB_URL, connect_args={'check_same_thread': False})
engine = create_engine(settings.DB_URL)#, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()




Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# @contextmanager
# def get_session():
#     session = SessionLocal()
#     try:
#         yield session
#         session.commit()

#     except Exception as e:
#         session.rollback()
#         print('Error: ',e)
#         raise

#     finally:
#         session.close()
