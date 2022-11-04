from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import null, text
from.database import Base

class DB_Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.user_id", ondelete="NO ACTION"), nullable=False)
    post_title = Column(String, nullable=False)
    post_content = Column(String, nullable=False)
    post_category = Column(String, nullable=False)
    post_published = Column(Boolean, server_default='FALSE', nullable=False)
    post_date = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    post_published_by = relationship("DB_User")

class DB_User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    user_email = Column(String, nullable=False, unique=True)
    user_pwd = Column(String, nullable=False)
    user_createdate = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)