from hashlib import md5

from fastapi import HTTPException

from backend.service.api.repositories.base import AbstractRepository
from backend.service.api.schemas import UserLogin, UserRegister, SignInResponse, User
from backend.service.api.db import DBUser
from backend.service.api.repositories.user_repo import UserRepository
from backend.service.api.security import create_access_token


class AuthService:
    def __init__(self, user_repo: AbstractRepository):
        self.users_repo: AbstractRepository = user_repo

    async def sign_in(self, user: UserLogin):

        db_user: DBUser = await self.users_repo.find_by_options(username=user.username, unique=True)

        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if db_user.hash_password != md5(user.password.encode('utf-8')).hexdigest():
            raise HTTPException(status_code=403, detail="Password is incorrect")

        user: User = User(id=db_user.id, username=db_user.username)

        access_token = create_access_token(user)

        return SignInResponse(access_token=access_token,
                              user_info=User(id=db_user.id,
                                             username=db_user.username))

    async def sign_up(self, user: UserRegister):

        db_user = await self.users_repo.find_by_options(username=user.username, unique=True)

        if db_user is not None:
            raise HTTPException(status_code=403, detail="User already exists")

        user_id = await self.users_repo.add(data={"username": user.username,
                                                  "hash_password": md5(user.password.encode('utf-8')).hexdigest(),
                                                  "user_email": user.email})

        user: User = User(id=user_id, username=user.username)

        access_token = create_access_token(user)

        return SignInResponse(access_token=access_token, user_info=user)


def auth_service():
    return AuthService(UserRepository())
