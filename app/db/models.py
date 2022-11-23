# For the SQLAlchemy model
from sqlalchemy.orm import backref, relationship
from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Text

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

#class Association(Base):
#    __tablename__ = "association_table"
#    left_id = Column(ForeignKey("labels.id"), primary_key=True)
#    right_id = Column(ForeignKey("articles.id"), primary_key=True)
#    label = relationship("Category", back_populates="all_articles")
#    article = relationship("Article", back_populates="all_labels")

association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("labels.id"), primary_key=True),
    Column("right_id", ForeignKey("articles.id"), primary_key=True),
)

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    isposted = Column(Boolean, default=False)
    title = Column(String(100), nullable=False)
    author_1 = Column(String(50), nullable=True)
    author_2 = Column(String(50), nullable=True)
    image = Column(String(100), nullable=True)
    content = Column(Text(5000))
    all_labels = relationship("Category", secondary=association_table, back_populates="all_articles")

class Category(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, index=True)
    all_articles = relationship("Article", secondary=association_table, back_populates="all_labels")
