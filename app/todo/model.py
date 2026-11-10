from pydantic import BaseModel




class TodoRequest(BaseModel):
    title: str
    description: str
    priority: int
    complete: bool