from .login import login_router
from .users import users_router
from .signup import signup_router
from .articles import article_router

from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(login_router.router, prefix="/login", tags=["login"])
api_router.include_router(users_router.router, prefix="/users", tags=["user"])
api_router.include_router(signup_router.router, prefix="/signup", tags=["signup"])
api_router.include_router(article_router.router, prefix="/article", tags=["article"])
