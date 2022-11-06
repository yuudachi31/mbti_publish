from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .. import schemas
from db import database
from ..login import login_router

router = APIRouter()

async def get_current_user(token: str = Depends(login_router.oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_expection = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
            )
    try:
        payload = jwt.decode(token, login_router.SECRET_KEY, algorithms = login_router.ALGORITHM)
        username: str = payload.get("sub")
        if not username:
            raise credentials_expection
        token_data = schemas.TokenData(username=username)

    except JWTError:
        raise credentials_expection

    user = login_router.get_user(db, username=token_data.username)
    if not user:
        raise credentials_expection

    return user

async def get_current_active_user(user: schemas.User = Depends(get_current_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid User")
    return user

@router.get("/me")
async def read_user(user: schemas.User = Depends(get_current_active_user)):
    return user
