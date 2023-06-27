from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todos
from database import SessionLocal
from starlette import status
from .auth import get_current_user


router = APIRouter()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# import dari auth routers
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
  title: str = Field(min_length=3)
  description: str = Field(min_length=3, max_length=100) 
  priority: int = Field(gt=0, lt=6)
  complete: bool

# GET DATA
# get data must authentication
@router.get("/")
async def read_all(user: user_dependency, db: db_dependency):
  return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

# get data by id must authentication
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):    # library Path -> untuk validation
  if user is None:
    raise HTTPException(status_code=401, detail='Auth Failed')

  todo_model = db.query(Todos).filter(Todos.id == todo_id)\
    .filter(Todos.owner_id == user.get('id')).first()
  if todo_model is not None:
    return todo_model
  raise HTTPException(status_code=404, detail='Todo Not Found')

# POST DATA
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest):
  if user is None:
    raise HTTPException(status_code=401, detail='Auth Failed')
  todo_model = Todos(**todo_request.dict(), owner_id=user.get('id'))
  
  db.add(todo_model)
  db.commit()

# PUT/ UPDATE DATA
# put using auth jwt
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
  if user is None:
    raise HTTPException(status_code=401, detail='Auth Failed')

  todo_model = db.query(Todos).filter(Todos.id == todo_id)\
    .filter(Todos.owner_id == user.get('id')).first()
  if todo_model is None:
    raise HTTPException(status_code=404, detail='Todo Not Found')
  
  todo_model.title = todo_request.title
  todo_model.description = todo_request.description
  todo_model.priority = todo_request.priority
  todo_model.complete = todo_request.complete
  
  db.add(todo_model)
  db.commit()
  
# DELETE DATA
# delete using auth jwt
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
  if user is None:
    raise HTTPException(status_code=401, detail='Auth Failed Bro')

  todo_model = db.query(Todos).filter(Todos.id == todo_id)\
    .filter(Todos.owner_id == user.get('id')).first()
  if todo_model is None:
    raise HTTPException(status_code=404, detail='Todo Not Found')
  db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
  
  db.commit()