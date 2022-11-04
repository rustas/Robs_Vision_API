from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import models
from . import schemas, database
from .config import settings


oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# openssl rand -hex 32
SECRET_KEY = settings.RV_API_SK
ALGORITHM = settings.RV_API_ALG
TOKEN_EXPIRE_TIME_MINUTES = settings.RV_API_TOKEN_TIMEOUT

def create_auth_token(payload: dict):
    TO_ENCODE = payload.copy()
    TOKEN_EXPIRE = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_TIME_MINUTES)
    TO_ENCODE.update({"exp": TOKEN_EXPIRE})
    ENCODED_TOKEN = jwt.encode(TO_ENCODE, SECRET_KEY, algorithm=ALGORITHM)
    return(ENCODED_TOKEN)

def verify_access_token(VERIFY_ACCESS_TOKEN: str, cred_exceptions):
    try:
        PAYLOAD = jwt.decode(VERIFY_ACCESS_TOKEN, SECRET_KEY, algorithms=[ALGORITHM])
        PAYLOAD_ID: str = PAYLOAD.get("user_id")
        if PAYLOAD_ID is None:
            raise cred_exceptions
        TOKEN_DATA = schemas.TokenData(user_id=PAYLOAD_ID)
    except JWTError:
        raise cred_exceptions

    return TOKEN_DATA

def get_current_user(GET_CURRENT_USER_TOKEN: str = Depends(oath2_scheme), db: Session = Depends(database.get_db)):
    cred_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWWW-Authenticate": "Bearer"})
    CURRENT_USER_TOKEN = verify_access_token(GET_CURRENT_USER_TOKEN, cred_exceptions)
    CURRENT_USER = db.query(models.DB_User).filter(models.DB_User.user_id == CURRENT_USER_TOKEN.user_id).first()
    return CURRENT_USER
    # return(verify_access_token(GET_CURRENT_USER_TOKEN, cred_exceptions))
    