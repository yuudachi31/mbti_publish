#For the Pydantic model
from typing import Literal, Optional
from pydantic import BaseModel, Json, JsonWrapper, validator
from pydantic.types import JsonMeta

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    email: str
    admin: bool

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    disabled: bool

    class Config:
        orm_mode = True

class ArticleRequestSchema(BaseModel):
    be_posted: bool
    label: list[int]
    title: str
    author_1: Optional[str] = None
    author_2: Optional[str] = None
    image: str
    content: str

class ArticleResponseSchema(ArticleRequestSchema):
    id: int

    class Config:
        orm_mode = True
