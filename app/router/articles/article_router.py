import db.models as orm_models

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from .. import schemas
from db import database, db_article_library
from ..users import users_router

router = APIRouter()

def create_new_article(db: Session, article: schemas.ArticleRequestSchema):
    new_article = orm_models.Article(
            publish = article.publish, 
            articleTitle = article.articleTitle, 
            articleDescription = article.articleDescription,
            date = article.date,
            date2 = article.date2,
            author_1 = article.author_1, 
            author_2 = article.author_2, 
            image = article.image, 
            articleContent = article.articleContent,
    )

    db.add(new_article)

    db.commit()

    db.refresh(new_article)

    all_labels = db_article_library.get_all_label(db, article.tags)

    for label in all_labels:
        new_article.all_tags.append(label)

    db.commit()

    return new_article


@router.get('/feed', response_model=List[schemas.ArticleLabelResponseSchema])
def feed_initial_labels(db: Session = Depends(database.get_db)):
    return db_article_library.db_feed(db)

@router.get('/article_id', response_model=schemas.ArticleResponseWithLabelSchema)
def get_article_by_id(id: int, db: Session = Depends(database.get_db)):
    return db_article_library.get_article_by_id(id=id, db=db)
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

@router.get("/tags", response_model=List[schemas.ArticleLabelResponseSchema])
def get_article_labels_from_association_table(id: int, db: Session = Depends(database.get_db)):
    labels = db_article_library.get_article_labels_from_association_table(id, db)
    if not labels:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Article with id = {id} not found')
    return labels

@router.get("/filterarticle", response_model=List[schemas.ArticleResponseSchema])
def get_filter_article(tags: List[int] = Query(...), db: Session = Depends(database.get_db)):
    articles = db_article_library.get_article_by_labels(label=tags, db=db)
    if not articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Article with label = {tags} not found')
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

@router.post('/comment', response_model=schemas.CommentResponse)
def post_comment(commentContent: schemas.CommentRequest, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(users_router.get_current_user)):
    credentials_expection = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
            )
    comment = None
    if current_user and current_user.id == commentContent.owner_id:
        comment = db_article_library.db_post_comment(db, commentContent)
    else:
        raise credentials_expection
    return comment

@router.put('/like', response_model=schemas.LikeResponse)
def click_like(likeContent: schemas.LikeRequest, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(users_router.get_current_user)):
    credentials_expection = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
            )
    none_expection = HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="No return",
        headers={"WWW-Authenticate": "Bearer"}
            )
    like = None
    if current_user and current_user.id == likeContent.owner_id:
        like = db_article_library.db_like_update(db, likeContent)
    else:
        raise credentials_expection

    if like:
        return like
    else:
        raise none_expection


@router.delete('/DeleteArticle')
def delete_article(article_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(users_router.get_current_user)):
    credentials_expection = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
            )
    if current_user.admin == True:
        db_article_library.db_delete_article(article_id, db)
    else:
        raise credentials_expection
    return {"Success"}
