from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Optional, List
from blog.database import engine, SessionLocal, get_db
from blog import models
from blog.schemas import Blog, ResponseBlog, CreateUser, ResponseUser
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from blog.routers import blog

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.include_router(blog.router)
#app.include_router(blog.router)

@app.get("/", tags=["App Status"])
def status():
    return {"Status": "OK"}


# @app.post('/blog', status_code=201, tags=["Create Blog"])
# def create_blog(blog: Blog, db: Session = Depends(get_db)):
#     new_blog = models.Blog(title=blog.title, body=blog.body, user_id=1)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     db.close()
#     return new_blog


# @app.get('/all_blogs', response_model=List[ResponseBlog], tags=["Get All Blogs"])
# async def get_all_blogs(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs





@app.delete("/delete_blog/{id}", tags=["Delete Blog"])
async def delete_blog_by_id(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return "Done"


@app.post("/create_user", tags=["Create User"])
async def create_user(create_user: CreateUser, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(create_user.password)
    new_user = models.User(name=create_user.name, email=create_user.email, password=hashed_password, )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user


@app.get("/get_users", response_model=List[ResponseUser], tags=["Get Users"])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
