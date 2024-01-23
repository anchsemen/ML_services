from fastapi import HTTPException

from backend.service.api.repositories.base import SQLAlchemyRepository
from backend.service.api.repositories.prediction_repo import PredictionRepository
from backend.service.api.repositories.predictor_repo import PredictorRepository
from backend.service.api.repositories.user_repo import UserRepository
from backend.service.api.tasks.make_prediction import run_model


class PredictionService:
    def __init__(self,
                 prediction_repo: SQLAlchemyRepository,
                 predictor_repo: SQLAlchemyRepository,
                 user_repo: SQLAlchemyRepository):
        self.prediction_repo: SQLAlchemyRepository() = prediction_repo
        self.predictor_repo: SQLAlchemyRepository() = predictor_repo
        self.user_repo: SQLAlchemyRepository() = user_repo

    async def get_prediction(self, user_id: int, model: str, input_data: str):
        db_predictor = await self.predictor_repo.find_by_options(name=model, unique=True)
        db_user = await self.user_repo.find_by_options(id=user_id, unique=True)

        if db_predictor is None:
            raise HTTPException(status_code=404, detail="Predictor not found")

        if db_user.balance < db_predictor.cost:
            raise HTTPException(status_code=400, detail="Not enough balance")

        await self.user_repo.update({"balance": db_user.balance - db_predictor.cost}, id=user_id)
        prediction_data = {"predictor_id": db_predictor.id, "user_id": user_id}
        prediction_id = await self.prediction_repo.add(data=prediction_data)

        run_model(prediction_id, db_predictor.filename, db_user.id, db_user.balance, input_data)

        return prediction_id


def prediction_service():
    return PredictionService(prediction_repo=PredictionRepository(),
                             predictor_repo=PredictorRepository(),
                             user_repo=UserRepository())
