from fastapi import status, Depends, HTTPException, Response, APIRouter
from typing import List, Optional
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import Post as PostSchema, PostCreate, PostOutput
from app.models import Post as PostModel
from app.models import Vote
from app.oauth2 import get_current_user
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Post"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostSchema)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user= Depends(get_current_user)): #type:ignore
    new_post = PostModel(**post.model_dump(), user_id = current_user.id)
    db.add(new_post)
    db.commit() 
    db.refresh(new_post)
    return new_post

@router.get("/", response_model=List[PostOutput])
def get_all_posts(db: Session = Depends(get_db), current_user = Depends(get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""): #type:ignore
    posts = db.query(PostModel, func.count(Vote.post_id)).join(Vote, Vote.post_id == PostModel.id, isouter=True).group_by(PostModel.id).filter(PostModel.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/{id}", response_model=PostOutput)
def get_specific_post(db: Session = Depends(get_db), current_user = Depends(get_current_user)): #type:ignore
    post_query = db.query(PostModel, func.count(PostModel.id).label("vote")).join(Vote, Vote.post_id == PostModel.id, isouter=True).group_by(PostModel.id).filter(PostModel.id == current_user.id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    if (post.user_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform the requested action")
    return post


@router.put("/{id}", response_model=PostSchema)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db),current_user = Depends(get_current_user)): #type:ignore
    post_query = db.query(PostModel).filter(PostModel.id == current_user.id)
    updated_post = post_query.first()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    if (updated_post.user_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform the requested action")
    post_query.update(post.model_dump(), synchronize_session=False) # type: ignore
    db.commit()
    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)): #type:ignore
    post_query = db.query(PostModel).filter(PostModel.id == id)
    deleted_post = post_query.first()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    if (deleted_post.user_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform the requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)