from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, database, oauth2

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), CURRENCT_USER: int = Depends(oauth2.get_current_user)):
    POST_EXISTS = db.query(models.DB_Post).filter(models.DB_Post.id == vote.post_id, models.DB_Post.post_published == True).first()
    print(POST_EXISTS)
    if not POST_EXISTS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {vote.post_id} does not exists")
    VOTE_QUESRY = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == CURRENCT_USER.user_id)
    FOUND_VOTE = VOTE_QUESRY.first()
    if (vote.dir == 1):
        if FOUND_VOTE:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User: {CURRENCT_USER.user_id} has already voted on post: {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id=CURRENCT_USER.user_id)
        db.add(new_vote)
        db.commit()
        return({"message": "succcessfully added vote"})
    else:
        if not FOUND_VOTE:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exists")
        VOTE_QUESRY.delete(synchronize_session=False)
        db.commit()
        return({"message": "successfully delete vote"})