from backend.service.api.repositories.base import SQLAlchemyRepository
from backend.service.api.db import DBPredictor


class PredictorRepository(SQLAlchemyRepository):
    model = DBPredictor
