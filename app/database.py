from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean

from .config import settings

SQL_ALCHEMY_DB_URL = f"postgresql://{settings.RV_API_UID}:{settings.RV_API_PWD}@{settings.RV_API_SRV_URL}/{settings.RV_API_DB}"

#IF SQL LITE DB, connect_args={"check_same_thread": False}
engine = create_engine(SQL_ALCHEMY_DB_URL)
LOCAL_SESSION = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = LOCAL_SESSION()
    try:
        yield db
    finally:
        db.close()