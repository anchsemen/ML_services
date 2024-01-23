from backend.service.api.repositories.base import SQLAlchemyRepository
from backend.service.api.db import DBUser


class UserRepository(SQLAlchemyRepository):
    model = DBUser
