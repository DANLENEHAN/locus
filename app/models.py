from sqlalchemy import (
    Column, Integer, String
)
from sqlalchemy.orm import declarative_base

# declarative base class
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False)
    password = Column(String(100), nullable=False)
