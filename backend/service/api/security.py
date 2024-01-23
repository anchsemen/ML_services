from datetime import datetime, timezone, timedelta
from typing import Union
from fastapi import HTTPException, Depends, status, Cookie
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from backend.service.api.schemas import User

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

bearer_scheme = HTTPBearer()


def create_access_token(user: User) -> str:
    data = user.model_dump()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Union[str, HTTPAuthorizationCredentials] = Depends(bearer_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user_id: str = payload.get("id")

        if username is None or user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return User(id=user_id, username=username)


async def get_current_user_from_cookie(access_token=Cookie(None)):
    if access_token is not None:
        user = await get_current_user(access_token)
        return user
    else:
        raise HTTPException(status_code=status.HTTP_307_TEMPORARY_REDIRECT, headers={'Location': '/auth'})
