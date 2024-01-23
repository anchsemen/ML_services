from backend.service.api.repositories.base import SQLAlchemyRepository
from backend.service.api.db import DBPrediction


class PredictionRepository(SQLAlchemyRepository):
    model = DBPrediction
