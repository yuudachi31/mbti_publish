# For the SQLAlchemy model
from sqlalchemy.orm import backref, relationship
from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Text

#class Admin(Base):
#    __tablename__ = "admin"
#
#    id = Column(Integer, primary_key=True, index = True)
#    username = Column(String, unique=True, index = True)
#    email = Column(String, unique=True, index = True)
#    disabled = Column(Boolean, default=False)
#    hashed_password = Column(String)
    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, unique=True, index=True)
    email = Column(Text, unique=True, index=True)
    hashed_password = Column(Text)
    disabled = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)

association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("tags.id"), primary_key=True),
    Column("right_id", ForeignKey("articles.id"), primary_key=True),
)

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    publish = Column(Boolean, default=False)
    articleTitle = Column(Text, nullable=False)
    articleDescription = Column(Text, nullable=True)
    date = Column(Text, nullable=True)
    date2 = Column(Text, nullable=True)
    author_1 = Column(Text, nullable=True)
    author_2 = Column(Text, nullable=True)
    image = Column(Text, nullable=True)
    articleContent = Column(Text)
    all_tags = relationship("Category", secondary=association_table, back_populates="all_articles")

class Category(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    tag = Column(Text, index=True)
    all_articles = relationship("Article", secondary=association_table, back_populates="all_tags")
