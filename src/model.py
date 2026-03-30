from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import Base

class User(Base):

    __tablename__ = 'users'

    id=Column(Integer, primary_key=True)
    name =Column(String(50),nullable=False)
    email=Column(String(50),nullable=False,unique=True)
    created_at=Column(DateTime,nullable=False)

class Post(Base):

    __tablename__ = 'posts'

    id=Column(Integer, primary_key=True)
    title=Column(String(100),nullable=False)
    content=Column(String(500),nullable=False)
    user_id=Column(Integer,nullable=False)
    created_at=Column(DateTime,nullable=False)


