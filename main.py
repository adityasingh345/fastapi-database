from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated

# models-> your SQLAlchemy ORM models
import models

from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

# it reads all sqlalchemy models, creates tables in the database if they dont exist rune once at startup 
models.Base.metadata.create_all(bind=engine)

# request Bodies Post Schemas
# defines expected JSON structureused for creating post and validationg input automatically
class PostBase(BaseModel):
    title: str
    content: str
    user_id: int
    
# used when creating user 
class UserBase(BaseModel):
    username: str

#creates a new db session per request
#yield db -> fastapi injects it itno endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()
        
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.post('/posts/')
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()


@app.post('/users', status_code=status.HTTP_201_CREATED)
async def create_user(user:UserBase, db:db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    
@app.get('/users/{user_id}', status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db : db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='user not found') 
    return user