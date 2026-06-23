from fastapi import APIRouter, status, Depends, HTTPException
from app.database import get_db
from typing import Any
from sqlalchemy.orm import Session
from app.models import Vote
from app.schemas import VoteClass
from app.oauth2 import get_current_user

router = APIRouter(prefix="/vote",tags=["Vote"])

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: VoteClass, db: Session = Depends(get_db), current_user: Any = Depends(get_current_user)):
    vote_query = db.query(Vote).filter(Vote.post_id == vote.post_id, Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User: {current_user.user_id} has already casted vote on the post: {Vote.post_id}")
        new_vote = Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return{"status":"upvoted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cannot downvote on a non- voted post")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"status":"downvoted"}