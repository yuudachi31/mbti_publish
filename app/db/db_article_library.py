from typing import List
from sqlalchemy import true
from sqlalchemy.orm import Session
from fastapi import HTTPException, Query, status
from .mbti_feed import labels
import db.models as orm_models

def db_feed(db: Session):
    new_label_list = [orm_models.Category(
        label=feed_label["label"]
        ) for feed_label in labels]
    db.query(orm_models.Category).delete()
    db.commit()
    db.add_all(new_label_list)
    db.commit()
    return db.query(orm_models.Category).all()

def db_update_article(db: Session, update_content: orm_models.Article):
    article = db.query(orm_models.Article).filter(orm_models.Article == update_content.article_id)
    if hasattr(update_content, 'isposted'): 
        article.update({
            orm_models.Article.isposted: update_content.isposted,
            })

    if "title" in update_content:
        print("Change title")
        article.update({
            orm_models.Article.title: update_content.title
            })

    if "author_1" in update_content:
        print("Change author_1")
        article.update({
            orm_models.Article.author_1: update_content.author_1
            })
    if "author_2" in update_content:
        print("Change author_2")
        article.update({
            orm_models.Article.author_2: update_content.author_2
            })

    if "image" in update_content:
        print("Change image")
        article.update({ orm_models.Article.image: update_content.image})

    if "content" in update_content:
        print("Change content")
        article.update({ orm_models.Article.content: update_content.content})

    if "labels" in update_content:
        article_detail = db.query(orm_models.Article).filter(orm_models.Article.id == update_content.article_id).first()
        article_detail.all_labels.clear()
        all_labels = get_all_label(db, update_content.labels)
        for label in all_labels:
            article_detail.all_labels.append(label)

    db.commit()

    new_article = db.query(orm_models.Article).filter(orm_models.Article.id == update_content.article_id).first()

    return new_article


    

def get_all_label(db: Session, labels: List[int]):
    all_labels = []
    for label in labels:
        all_labels.append(db.query(orm_models.Category).filter(orm_models.Category.id == label).first())

    return all_labels

def get_all_article(db: Session):
    return db.query(orm_models.Article).all()

def get_all_post_article(db: Session) -> list[orm_models.Article]:
    articles = db.query(orm_models.Article).filter(orm_models.Article.isposted == True).all()
    return articles

def get_ten_post_article(db: Session, begin_id: int):
    return db.query(orm_models.Article).filter(orm_models.Article.id <= begin_id).all()

def get_article_by_id(id: int, db: Session):
    article = db.query(orm_models.Article).filter(orm_models.Article.id == id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article with id = {id} not found")
    return article

def get_article_by_labels(db: Session, label: List[int] = Query(...)) -> list[orm_models.Article]:
    all_articles_id = []
    for label_id in label:
        for left_id in db.query(orm_models.association_table).filter(orm_models.association_table.c.left_id == label_id).all():
            all_articles_id.append(left_id[1])
    all_articles_id = list(dict.fromkeys(all_articles_id))
    all_articles = []
    for id in all_articles_id:
        all_articles.append(db.query(orm_models.Article).filter(orm_models.Article.id == id).first())
    return all_articles

def get_article_labels_from_association_table(id: int, db: Session) -> list[orm_models.Category]:
    all_association = db.query(orm_models.association_table).filter(orm_models.association_table.c.right_id == id).order_by(orm_models.association_table.c.left_id.asc()).all() 
    all_labels = []
    for label in all_association:
        all_labels.append(db.query(orm_models.Category).filter(orm_models.Category.id == label[0]).first())
    return all_labels
