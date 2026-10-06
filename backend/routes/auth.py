from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from scheme import UserSignup, UserLogin
from database import get_db
from sqlalchemy.orm import Session
from security import hashed_password, verify_password, get_current_user, get_user_token
from model import User


router = APIRouter(prefix="/auth")

@router.post("/signup")
def signup(userData:UserSignup, db:Session = Depends(get_db)):
    user_email = userData.email
    existing_user = db.query(User).filter(User.email== userData.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="User already exist!" 
            )
    hashed = hashed_password(userData.password)
    new_user = User(
        name=userData.name,
        email=userData.email,
        password=hashed
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message":"User Profile Created successfully"
    }

@router.post("/login")
def login(form_data:OAuth2PasswordRequestForm=Depends(), db:Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.email==form_data.username).first()
    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    verified = verify_password(form_data.password, existing_user.password)
    if not verified:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid Credentials"
        )
    token = get_user_token(existing_user.id) 
    return {
        "access_token":token,
        "token_type":"Bearer"
    }

@router.get("/me")
def userProfile(user = Depends(get_current_user)):
    return {
        "Name":user.name,
        "email":user.email
    }