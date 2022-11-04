from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/new", status_code=status.HTTP_201_CREATED, response_model=schemas.UserReturn)
def create_user(user_new: schemas.UserNew, db: Session = Depends(get_db)):
    sec_pwd = utils.pwd_hash(user_new.user_pwd)
    user_new.user_pwd = sec_pwd
    SQL_RETURN = models.DB_User(**user_new.dict())
    db.add(SQL_RETURN)
    db.commit()
    db.refresh(SQL_RETURN)
    return( SQL_RETURN )

@router.get("/{id}", response_model=schemas.UserReturn)
def GET_USER_BY_ID(id: int, db: Session = Depends(get_db)):
    SQL_RETURN = db.query(models.DB_User).filter(models.DB_User.user_id == id).first()
    if not SQL_RETURN:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with {id} does not exists")

    return(SQL_RETURN)