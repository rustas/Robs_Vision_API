from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2
router = APIRouter(tags=['Auth'])

@router.post("/login", response_model=schemas.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    SQL_RETURN = db.query(models.DB_User).filter(models.DB_User.user_email == user_cred.username).first()
    if not SQL_RETURN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials.")
    if not utils.pwd_verify(user_cred.password, SQL_RETURN.user_pwd):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials.")
    ACCESS_TOKEN = oauth2.create_auth_token(payload = {"user_id": SQL_RETURN.user_id })
    return({"access_token": ACCESS_TOKEN, "token_type": "Bearer"})