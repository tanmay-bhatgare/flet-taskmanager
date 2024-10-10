import enum
from sqlalchemy import Column, DateTime, Enum, Integer, String, Boolean, text
from ..db.database import Base


class User(Base):
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(24), nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    joined_at = Column(DateTime, server_default=text("NOW()"), nullable=False)