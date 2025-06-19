# routes/protected.py
from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user

router = APIRouter()

@router.get("/me")
def read_users_me(user=Depends(get_current_user)):
    return {"username": user.username}