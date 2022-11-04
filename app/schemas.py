from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    post_title: str
    post_content: str
    post_category: str
    post_published: bool = False

class UserReturn(BaseModel):
    user_id: int
    user_email: EmailStr
    user_createdate: datetime
    class Config:
        orm_mode = True

class PostCreate(PostBase):
    pass

class PostReturn(PostBase):
    post_date: datetime
    id: int
    owner_id: int
    post_published_by: UserReturn
    class Config:
        orm_mode = True

class UserNew(BaseModel):
    user_email: EmailStr
    user_pwd: str

class UserLogin(BaseModel):
    user_email: EmailStr
    user_pwd: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)