from pydantic import HttpUrl
from pwdlib import PasswordHash
from dotenv import load_dotenv
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import os
from database import get_db
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status
from model import User


load_dotenv()
ALGORITHM = os.getenv("ALGORITHM")
SECRET_CODE = os.getenv("SECRET_CODE")
passwordhash = PasswordHash.recommended()

def verify_password(user_password, hashed_password):
    return passwordhash.verify(user_password, hashed_password)

def hashed_password(user_password):
    return passwordhash.hash(user_password)

def get_user_token(user_id):
    expire = datetime.now(timezone.utc)+timedelta(minutes=30)
    payload = {
        "sub":str(user_id),
        "exp":expire
    }
    token = jwt.encode(
        payload,
        SECRET_CODE,
        algorithm=ALGORITHM
    )
    return token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token: str = Depends(oauth2_scheme), db:Session =Depends(get_db)):
    payload = jwt.decode(
        token, 
        SECRET_CODE, 
        algorithms=[ALGORITHM]
    )
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "User not Authorised"
            )
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UnAuthorized User"
        )
    return user
