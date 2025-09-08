from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing  import Optional
from pydantic.types import conint
from .models import Post




class postbase(BaseModel):
    title: str
    content: str
    published: bool = True 

class PostCreate(postbase):
    pass

class responseUser(BaseModel):
    id : int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class responsePost(postbase):
    id : int
    created_at: datetime
    owner_id : int
    owner : responseUser
    
    class Config:
        orm_mode = True 

class PostOut(BaseModel):
    Post : responsePost
    votes : int 

    class config:
        orm_mode = True 




class UserCreate(BaseModel):
    email: EmailStr
    password: str 

  
class responselogin(BaseModel):
    email: EmailStr
    password: str


class token(BaseModel):
    access_token : str
    token_type : str

class tokendata(BaseModel):
    id : int

class vote(BaseModel):
    post_id : int
    dir : conint(le=1)






