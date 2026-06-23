from fastapi import HTTPException, APIRouter, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Any
from app.schemas import Token
from app.oauth2 import create_access_token
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import Users
from app.utils import verify_password

router = APIRouter(tags=['Authentication'])

@router.post("/login",response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)) -> dict[str, Any]:
    user_query = db.query(Users).filter(Users.email == user_credentials.username)
    user = user_query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid Credentials"
        )
    if not verify_password(user_credentials.password, user.password): # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid Credentials"
        )
    access_token = create_access_token(data={"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}
