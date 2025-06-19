# routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from schemas.user import UserCreate, Token
from models.user import User
from auth.jwt import create_access_token
from datetime import timedelta
from config import ACCESS_TOKEN_EXPIRE_MINUTES
import hashlib

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pw = hashlib.sha256(user.password.encode()).hexdigest()
    new_user = User(username=user.username, hashed_password=hashed_pw)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"msg": "User created"}

@router.post("/login", response_model=Token)
def login(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if not db_user or db_user.hashed_password != hashlib.sha256(user.password.encode()).hexdigest():
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}
