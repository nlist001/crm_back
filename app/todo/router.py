
from fastapi import  APIRouter, Body, HTTPException, Path, Query, Response

# from auth.auth import current_user_dependency, credentials_exception
# from db import db_dependency
# from todo.model import TodoRequest
# from todo.schemas import TodoTable


router = APIRouter(
    tags=["todo"]
)


@router.get("/test")
async def get_todos(response:Response):
    response.headers['marco'] = 'polo'
    return "res body"

# @router.get("/todos")
# async def get_todos(current_user: current_user_dependency, db: db_dependency):
#     return db.query(TodoTable).all()

# @router.get("/todos/{id}")
# async def get_todos_by_id(current_user: current_user_dependency, db: db_dependency, id: int = Path(gt=0)):
#     print('db.query(TodoTable)1: ',db.query(TodoTable))

    
#     res = db.query(TodoTable).filter(TodoTable.id == id).first()
#     if not res:
#         raise HTTPException(status_code=404, detail="TodoTable not found")
#     return res


# @router.post("/todos")
# async def create_todos(
#     current_user: current_user_dependency, 
#     db: db_dependency, 
#     todo_request: TodoRequest
# ):

#     todo_model = TodoTable(**todo_request.model_dump(), owner_id=current_user.id)
#     db.add(todo_model)
#     db.commit()
#     db.refresh(todo_model)
#     return todo_model


# @router.put("/todos/{id}")
# async def update_todo(current_user: current_user_dependency, db: db_dependency,id:int, todo_request: TodoRequest):
#     todo_model = db.query(TodoTable).filter(TodoTable.id == id).first()
#     if not todo_model:
#         raise HTTPException(status_code=404, detail="TodoTable not found")
#     todo_data = TodoTable(**todo_request.model_dump())

#     todo_model.title = todo_data.title
#     todo_model.description = todo_data.description
#     todo_model.priority = todo_data.priority
#     todo_model.complete = todo_data.complete
#     db.add(todo_model)
#     db.commit()
#     return todo_model


# @router.delete("/Todos/{id}")
# async def delete_Todo(current_user: current_user_dependency,db: db_dependency,id:int):
#     todo_model = db.query(TodoTable).filter(TodoTable.id == id).first()
#     print(todo_model)
#     if not todo_model:
#         raise HTTPException(status_code=404, detail="TodoTable not found")

#     db.query(TodoTable).filter(TodoTable.id == id).delete()
#     db.commit()
#     return todo_model
