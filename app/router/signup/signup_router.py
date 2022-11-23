import db.models as orm_models


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..schemas import User as pydantic_user
from ..schemas import UserCreate
from db import database, db_user_library

router = APIRouter()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_user_in_db(db: Session, user: UserCreate):
    hased_password = hash_password(user.password)
    db_user = orm_models.User(username = user.username, email = user.email, hashed_password = hased_password, disabled = False, admin = user.admin)

    db.add(db_user)

    db.commit()

    db.refresh(db_user)
    return db_user

@router.post("/users", response_model=pydantic_user)
async def create_user(user: UserCreate, db: Session = Depends(database.get_db)):
    db_user = db_user_library.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The email have been used")
    res_user = create_user_in_db(db, user)
    return res_user
