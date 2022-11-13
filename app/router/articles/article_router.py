from typing import List, Optional
from fastapi import APIRouter, Depends
from pydantic import Json
from sqlalchemy.orm import Session
from .. import schemas
from db import database, db_article_library

router = APIRouter()

def get_articles_label(db: Session, label: int):
    return db_article_library.get_article_by_label(label, db)

@router.get('/all', response_model=List[schemas.ArticleResponseSchema])
def get_all_article(db: Session = Depends(database.get_db)):
    return db_article_library.get_all_article(db)

def create_new_article(db: Session, article: schemas.ArticleRequestSchema):
    pass

@router.post("/NewArticle", response_model=schemas.ArticleRequestSchema)
async def create_article(article: schemas.ArticleRequestSchema , db: Session = Depends(database.get_db)):
    return article
