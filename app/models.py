from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

# declarative base class
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    user_id = Column(String(32), primary_key=True, nullable=False)
    email = Column(String(30), nullable=False)
    password = Column(String(100), nullable=False)
