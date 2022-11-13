from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import db.models as orm_models

def get_all_article(db: Session):
    return db.query(orm_models.Article).all()

def get_article_by_id(id: int, db: Session):
    article = db.query(orm_models.Article).filter(orm_models.Article.id == id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article with id = {id} not found")
    return article

def get_article_by_label(label: List[int], db: Session):
    all_correspondence_article = []

    for lab in label:
        select_article = db.query(orm_models.Article).filter(orm_models.Article.label == lab).all()
        all_correspondence_article.append(select_article)

    return all_correspondence_article

