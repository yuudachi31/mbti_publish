from sqlalchemy.orm import Session

import db.models as orm_models


def get_user(db: Session, username: str):
    return db.query(orm_models.User).filter(orm_models.User.username == username).first()

def get_user_by_email(db: Session, email : str):
    return db.query(orm_models.User).filter(orm_models.User.email == email).first()
