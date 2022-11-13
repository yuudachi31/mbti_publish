from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from db import database, db_user_library
from .. import schemas

SECRET_KEY = "4aa4944891e2845a48f1ba19426004367d8ff6c008336855beb38b94f8070593"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def verify_password(plain_password, hased_password):
    return pwd_context.verify(plain_password, hased_password)

def authenticate_user(db: Session, username: str, password: str):
    user = db_user_library.get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user

def create_access_token(
        data: dict,
        expire_delta: Optional[timedelta] = None
        ):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

@router.get("/token")
async def read_token(token: str = Depends(oauth2_scheme)):
    return {"token": token}

@router.post("/token", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    username = form_data.username
    password = form_data.password

    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
    )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.username},
        expire_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type" : "bearer"}
