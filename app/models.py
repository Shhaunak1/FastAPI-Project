from sqlalchemy import Column, Integer, String, Boolean, text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

# Defining what Posts look like by creating a table in postgres called "posts"
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False, index=True)
    content = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False,index=True)
    published = Column(Boolean, server_default='TRUE',nullable=False, index=True)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text('now()'),nullable=False,index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    owner = relationship("Users")

# Handling users 
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String,unique=True,index=True,nullable=False)
    password = Column(String,nullable=False,index=True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,index=True,server_default=text('now()'))
    
class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"), primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), primary_key=True, nullable=False, index=True)