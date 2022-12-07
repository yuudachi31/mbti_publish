from typing import List
from sqlalchemy import true
from sqlalchemy.orm import Session
from fastapi import HTTPException, Query, status
from .mbti_feed import labels
from router.schemas import ArticleEditRequestSchema

import db.models as orm_models

def db_feed(db: Session):
    new_label_list = [orm_models.Category(
        tag=feed_label["label"]
        ) for feed_label in labels]
    db.query(orm_models.Category).delete()
    db.commit()
    db.add_all(new_label_list)
    db.commit()
    return db.query(orm_models.Category).all()

def db_update_article(db: Session, update_content: ArticleEditRequestSchema):
    article = db.query(orm_models.Article).filter(orm_models.Article.id == update_content.article_id)
    if update_content.publish != None: 
        article.update({
            orm_models.Article.publish: update_content.publish,
            })

    if update_content.articleTitle != None:
        article.update({
            orm_models.Article.articleTitle: update_content.articleTitle
            })

    if update_content.articleDescription != None:
        article.update({
            orm_models.Article.articleDescription: update_content.articleDescription
            })

    if update_content.author_1 != None:
        article.update({
            orm_models.Article.author_1: update_content.author_1
            })
    if update_content.author_2 != None:
        article.update({
            orm_models.Article.author_2: update_content.author_2
            })

    if update_content.image != None:
        article.update({ orm_models.Article.image: update_content.image})

    if update_content.articleContent != None:
        article.update({ orm_models.Article.articleContent: update_content.articleContent})

    if len(update_content.tags) > 0:
        article_detail = db.query(orm_models.Article).filter(orm_models.Article.id == update_content.article_id).first()
        article_detail.all_tags.clear()
        all_labels = get_all_label(db, update_content.tags)
        for label in all_labels:
            article_detail.all_tags.append(label)

    db.commit()

    new_article = db.query(orm_models.Article).filter(orm_models.Article.id == update_content.article_id).first()

    return new_article


def db_delete_article(id: int, db: Session):
    article = db.query(orm_models.Article).filter(orm_models.Article.id == id).first()
    if article:
        db.delete(article)
        db.commit()
    else:
        print("The article id doesn't exist")

def get_all_label(db: Session, labels: List[int]):
    all_labels = []
    for label in labels:
        all_labels.append(db.query(orm_models.Category).filter(orm_models.Category.id == label).first())

    return all_labels

def get_all_article(db: Session):
    return db.query(orm_models.Article).all()

def get_all_post_article(db: Session) -> List[orm_models.Article]:
    articles = db.query(orm_models.Article).filter(orm_models.Article.publish == True).all()
    return articles

def get_ten_post_article(db: Session, begin_id: int):
    articles = db.query(orm_models.Article).filter(orm_models.Article.publish == True).all()
    returnArticles = []
    for i in range(begin_id):
        if i >= len(articles):
            break
        returnArticles.append(articles[i])
    return returnArticles

def get_article_by_id(id: int, db: Session):
    article = db.query(orm_models.Article).filter(orm_models.Article.id == id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article with id = {id} not found")
    return article

def get_article_by_labels(db: Session, label: List[int] = Query(...)) -> List[orm_models.Article]:
    all_articles_id = []
    for label_id in label:
        for left_id in db.query(orm_models.association_table).filter(orm_models.association_table.c.left_id == label_id).all():
            all_articles_id.append(left_id[1])
    all_articles_id = list(dict.fromkeys(all_articles_id))
    all_articles = []
    for id in all_articles_id:
        all_articles.append(db.query(orm_models.Article).filter(orm_models.Article.id == id).first())
    return all_articles

def get_article_labels_from_association_table(id: int, db: Session) -> List[orm_models.Category]:
    all_association = db.query(orm_models.association_table).filter(orm_models.association_table.c.right_id == id).order_by(orm_models.association_table.c.left_id.asc()).all() 
    all_labels = []
    for label in all_association:
        all_labels.append(db.query(orm_models.Category).filter(orm_models.Category.id == label[0]).first())
    return all_labels
