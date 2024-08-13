from sqlalchemy import TIMESTAMP, Column, Integer, String, text,BigInteger,Text
from sqlalchemy.orm import relationship
from .database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer,nullable=False,primary_key=True)
    user_name = Column(String(255),nullable=False)
    email = Column(String(255),nullable=True,unique=True)
    avatar_url = Column(Text,nullable=True)
    github_id = Column(BigInteger,nullable=False)
    folder_name = Column(String(255), nullable=False, default='LeetCode')
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))
