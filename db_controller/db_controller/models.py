from sqlalchemy import (
    ForeignKey,
    Column,
    String,
    DateTime,
    Integer,
    Identity,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "app_user"
    username = Column(String, primary_key=True)
    password_hash = Column(String, nullable=False)


class Post(Base):
    __tablename__ = "post"
    id = Column("id", Integer, Identity(start=1, cycle=True), primary_key=True)
    title = Column(String)
    author = Column(String, ForeignKey("app_user.username"))
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())
    tagged_at = Column(DateTime(timezone=True), nullable=True)
    classification = Column(String, nullable=True)
