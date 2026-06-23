from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# Schemas/Pydantic models define the structure the request or response

class PostBase(BaseModel):
    title: str
    content: str
    category: str
    published: bool = True 

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id:int
    user_id:Optional[int] = None
    owner: UserOut
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)

class PostOutput(PostBase):
    Post: Post
    vote: int
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email:EmailStr
    password: str

class UserOut(BaseModel):
    email:EmailStr
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)

class UserAuth(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class VoteClass(BaseModel):
    post_id: int
    dir: bool