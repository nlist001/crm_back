from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.db import Base, engine

# from app.auth.model import *
#from todo.schemas import TodoTable
from app.models.users import *

from app.auth.router import router as authRouter
from todo.router import router as todoRouter
#from admin.router import router as admin_router
from app.dict.role import router as role_router
from app.dict.category import router as category_router
from app.dict.brands import router as brands_router
from app.dict.permission import router as permission_router
from app.users.router import router as users_router
from app.products.router import router as products_router
from app.stores.router import router as stores_router
from app.stores.cell.router import router as stores_cell_router
from app.stores.cell_stocks.router import router as stores_cell_stocks_router

# from sqlalchemy_data_model_visualizer import generate_data_model_diagram
# from app.models.users import PermissionTable, UserTable, UserRoleTable

# generate_data_model_diagram([UserTable, UserRoleTable, PermissionTable], output_file='my_data_model_diagram.svg',  add_labels=True)
# #add_web_font_and_interactivity('my_data_model_diagram.svg', 'my_interactive_data_model_diagram.svg')


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authRouter)
app.include_router(todoRouter)
# app.include_router(admin_router)
app.include_router(role_router)
app.include_router(category_router)
app.include_router(brands_router)
app.include_router(permission_router)
app.include_router(users_router)
app.include_router(products_router)
app.include_router(stores_cell_router)
app.include_router(stores_cell_stocks_router)
app.include_router(stores_router)




if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)