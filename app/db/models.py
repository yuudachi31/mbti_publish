# For the SQLAlchemy model
from .database import Base
from sqlalchemy import Boolean, Column, Integer, String

class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index = True)
    username = Column(String, unique=True, index = True)
    email = Column(String, unique=True, index = True)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String)
    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)

