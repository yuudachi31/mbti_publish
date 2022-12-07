#For the Pydantic model
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    email: EmailStr
    admin: bool

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    disabled: bool

    class Config:
        orm_mode = True

class ArticleBaseSchema(BaseModel):
    publish: bool
    articleTitle: str
    articleDescription: str
    date: str
    date2: str
    author_1: Optional[str] = None
    author_2: Optional[str] = None
    image: str
    articleContent: str

# From frontend get a list label id
class ArticleRequestSchema(ArticleBaseSchema):
    tags: List[int]

class ArticleEditRequestSchema(BaseModel):
    article_id: int
    publish: Optional[bool] = None
    articleTitle: Optional[str] = None
    articleDescription: Optional[str] = None
    author_1: Optional[str] = None
    author_2: Optional[str] = None
    image: Optional[str] = None
    articleContent: Optional[str] = None
    tags: Optional[List[int]] = None

# Just return the article without label
class ArticleResponseSchema(ArticleBaseSchema):
    id: int

    class Config:
        orm_mode = True

# Label base schema
class ArticleLabelRequestSchema(BaseModel):
    tag: str

# Just return label
class ArticleLabelResponseSchema(ArticleLabelRequestSchema):
    id: int

    class Config:
        orm_mode = True

# Return article with all labels
class ArticleResponseWithLabelSchema(ArticleBaseSchema):
    id: int
    all_tags: List[ArticleLabelResponseSchema]

    class Config:
        orm_mode = True

# Return label with all articles
class ArticleLabelResponseWithArticlesSchema(ArticleLabelRequestSchema):
    id: int
    articles: List[ArticleResponseSchema]

    class Config:
        orm_mode = True
