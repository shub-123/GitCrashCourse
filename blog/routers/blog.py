from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, database

router = APIRouter()


@router.get('/all_blogs', response_model=List[schemas.ResponseBlog], tags=["Get All Blogs"])
async def get_all_blogs(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get("/blog/{id}", status_code=200, response_model=schemas.ResponseBlog, tags=["Get Blog By ID"])
async def get_blog_by_id(id, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).where(models.Blog.id == id).first()
    if blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Id {id} not found"
        )
    return blog