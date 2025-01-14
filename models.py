from pydantic import BaseModel
from sqlalchemy.orm import relationship
from db import db
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
)
from datetime import datetime

from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    pelicula_favorita = Column(String, nullable=True)
    genero_favorito = Column(String, nullable=True)

    messages = relationship("Message", back_populates="user")


class Message(db.Model):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    content = Column(Text, nullable=False)
    author = Column(String, nullable=False)  # 'user' or 'assistant'
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="messages")


class Prompt(BaseModel):
    content: str
    movie: str
    year: int
    company: str
    is_vintage: bool
    is_specific: bool
    