from fastapi import APIRouter, Depends, status, HTTPException
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import UserCreate, UserOut
from app.utils import hash_password
from app.oauth2 import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Hash the password
    hashed_pwd = hash_password(user.password)
    
    # 2. Convert to dict
    user_data = user.model_dump()
    
    # 3. Reassign the hashed password. 
    # IMPORTANT: Change "password" to "hashed_password" if that is what 
    # your SQLAlchemy models.Users defines as the column name.
    user_data["password"] = hashed_pwd 
    
    # 4. Create the model instance
    new_user = models.Users(**user_data) 
    db.add(new_user)
    
    # 5. Safely attempt to commit to the database
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
        
    except IntegrityError:
        # If the email/username already exists, rollback the transaction and throw a 409
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="A user with these credentials already exists"
        )

@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db),current_user = Depends(get_current_user)): #type: ignore
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user