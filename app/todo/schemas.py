
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from typing import Optional

class TodoTable(Base):
    __tablename__='todo'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
