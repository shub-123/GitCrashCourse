from typing import Optional, List
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str
    published: Optional[bool]


class Blog(BlogBase):
    class Config():
        orm_mode = True


class ResponseUser(BaseModel):
    name: str
    email: str
    blogs : List[Blog] =[]
    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True


class ResponseBlog(BaseModel):
    title: str
    body: str
    creator: CreateUser

    class Config:
        orm_mode = True