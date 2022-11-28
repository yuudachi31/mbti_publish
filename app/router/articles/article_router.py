import db.models as orm_models

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic.schema import schema
from sqlalchemy.orm import Session
from sqlalchemy.sql import true
from .. import schemas
from db import database, db_article_library
from ..users import users_router

router = APIRouter()

def create_new_article(db: Session, article: schemas.ArticleRequestSchema):
    new_article = orm_models.Article(
            isposted = article.isposted, 
            title = article.title, 
            author_1 = article.author_1, 
            author_2 = article.author_2, 
            image = article.image, 
            content = article.content,
    )

    db.add(new_article)

    db.commit()

    db.refresh(new_article)

    all_labels = db_article_library.get_all_label(db, article.labels)

    for label in all_labels:
        new_article.all_labels.append(label)

    db.commit()

    return new_article


@router.get('/feed', response_model=List[schemas.ArticleLabelResponseSchema])
def feed_initial_labels(db: Session = Depends(database.get_db)):
    return db_article_library.db_feed(db)

# Get all article for admin
@router.get('/admin/all', response_model=List[schemas.ArticleResponseWithLabelSchema])
def get_all_article(db: Session = Depends(database.get_db)):
    return db_article_library.get_all_article(db)

# Get all article for user
@router.get('/user/all', response_model=List[schemas.ArticleResponseWithLabelSchema])
def get_all_post_article(db: Session = Depends(database.get_db)):
    return db_article_library.get_all_post_article(db)

# Get 10 article for user
@router.get('/user/{begin_id}', response_model=List[schemas.ArticleResponseSchema])
def get_ten_post_article(begin_id: int, db: Session = Depends(database.get_db)):
    return db_article_library.get_ten_post_article(db, begin_id)

# Create new article
@router.post("/NewArticle", response_model=schemas.ArticleResponseSchema)
def create_article(article: schemas.ArticleRequestSchema , db: Session = Depends(database.get_db)):
    new_article = create_new_article(db, article)
    return new_article

@router.get("/labels", response_model=List[schemas.ArticleLabelResponseSchema])
def get_article_labels_from_association_table(id: int, db: Session = Depends(database.get_db)):
    labels = db_article_library.get_article_labels_from_association_table(id, db)
    if not labels:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Article with id = {id} not found')
    return labels

@router.get("/filterarticle", response_model=List[schemas.ArticleResponseSchema])
def get_filter_article(labels: List[int] = Query(...), db: Session = Depends(database.get_db)):
    articles = db_article_library.get_article_by_labels(label=labels, db=db)
    if not articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Article with label = {labels} not found')
    return articles

@router.put('/edit', response_model=schemas.ArticleResponseWithLabelSchema)
def edit_article(update_content: schemas.ArticleEditRequestSchema, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(users_router.get_current_user)):
    credentials_expection = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
            )
    article = None
    if current_user.admin == True:
        article = db_article_library.db_update_article(db, update_content)
    else:
        raise credentials_expection
    return article
