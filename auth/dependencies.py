# auth/dependencies.py
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM
from schemas.user import UserRead
from database import get_session
from sqlmodel import select
from models.user import User


def get_current_user(token: str = Depends(lambda: ...), session=Depends(get_session)) -> User:
    # 这里你可以改成从 headers 中读取 token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user