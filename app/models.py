from sqlalchemy import TIMESTAMP, Column, Integer, String, text,BigInteger,Text
from .database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer,nullable=False,primary_key=True)
    user_name = Column(String(255),nullable=False)
    email = Column(String(255),nullable=True,unique=True)
    avatar_url = Column(Text,nullable=True)
    github_id = Column(BigInteger,nullable=False,unique=True)
    repo_name = Column(String(255), nullable=False, default='LeetCode')
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))
    
    def __repr__(self):
        return f"<Users id={self.id} user_name='{self.user_name}' github_id={self.github_id}>"

    def __str__(self):
        return self.__repr__()