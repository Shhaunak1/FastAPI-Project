# To generate a secure random secret key use the command on powershell:
# https://openssl.tplant.com.au/ (Online SSL Web Terminal)
# command: openssl rand -hex 32

from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError
from typing import Any, Dict
from datetime import datetime, timedelta, timezone
from app.schemas import TokenData
from fastapi.security import OAuth2PasswordBearer
from app import models
from app.database import get_db
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRATION_MINUTES = settings.access_token_expiration_time_in_minutes

def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes = ACCESS_TOKEN_EXPIRATION_MINUTES))
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str,credentials_exception:HTTPException)-> TokenData:
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id: int | None = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id = id)
    except (JWTError, ValidationError):
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    token_data = verify_token(token, credentials_exception)
    user = db.query(models.Users).filter(models.Users.id == token_data.id).first()
    if user is None:
        raise credentials_exception
    return user 