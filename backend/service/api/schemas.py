from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str


class SignInResponse(BaseModel):
    access_token: str
    user_info: User


class PredictorInfo(BaseModel):
    id: int
    name: str
    filename: str
    cost: int
