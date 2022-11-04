from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

from app import oauth2
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostReturn])
def GET_POSTS(db: Session = Depends(get_db), CURRENCT_USER: int = Depends(oauth2.get_current_user), post_count: int = 50, skip: int = 0, search: Optional[str] = ""):
    # models.DB_Post.post_published == True
    SQL_RETURN = db.query(models.DB_Post).filter(models.DB_Post.post_title.contains(search), models.DB_Post.post_published == True).limit(post_count).offset(skip).all()

    RESULTS = db.query(models.DB_Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.DB_Post.id, isouter=True).group_by(models.DB_Post.id).all()
    print(RESULTS)
    return( SQL_RETURN )

@router.get("/myposts", response_model=List[schemas.PostReturn])
def GET_POSTS(db: Session = Depends(get_db), CURRENCT_USER: int = Depends(oauth2.get_current_user)):
    SQL_RETURN = db.query(models.DB_Post).filter(models.DB_Post.owner_id == CURRENCT_USER.user_id).all()
    return( SQL_RETURN )

@router.get("/{id}", response_model=schemas.PostReturn)
def GET_POST_ID(id: int, db: Session = Depends(get_db), CURRENCT_USER: int = Depends(oauth2.get_current_user)):
    SQL_RETURN = db.query(models.DB_Post).filter((models.DB_Post.id == id and models.DB_Post.post_published == True)).first()
    if not SQL_RETURN:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} was not found")

    return( SQL_RETURN )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostReturn)
def NEW_POST(new_post: schemas.PostCreate, db: Session = Depends(get_db), CURRENCT_USER: int = Depends(oauth2.get_current_user)):
    try:
        SQL_RETURN = models.DB_Post(owner_id=CURRENCT_USER.user_id,**new_post.dict())
        db.add(SQL_RETURN)
        db.commit()
        db.refresh(SQL_RETURN)
        return( SQL_RETURN )

    except Exception as error:
        print("Failed to add new post.")
        print("Error: ", error)
        return({ "message:": "Failed to add new post." })


@router.put("/{id}")
def UPDATE_POST(id: int, update_post: schemas.PostCreate, db: Session = Depends(get_db), CURRENCT_USER: int = Depends(oauth2.get_current_user)):
    SQL_RETURN = db.query(models.DB_Post).filter(models.DB_Post.id == id)
    if SQL_RETURN.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} does not exists")

    if SQL_RETURN.first().owner_id != CURRENCT_USER.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You're not the owner of this post.")
    
    SQL_RETURN.update(update_post.dict(),synchronize_session=False)
    db.commit()
    return( SQL_RETURN.first() )

@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
def DELETE_POST(id: int, db: Session = Depends(get_db), CURRENCT_USER: int = Depends(oauth2.get_current_user)):
    SQL_RETURN = db.query(models.DB_Post).filter(models.DB_Post.id == id)
    if SQL_RETURN.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} does not exists")

    if SQL_RETURN.first().owner_id != CURRENCT_USER.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You're not the owner of this post.")

    SQL_RETURN.delete(synchronize_session=False)
    db.commit()
    return ( f"Deleted post with ID:{id}" )
    # Response(status_code=status.HTTP_204_NO_CONTENT)
    