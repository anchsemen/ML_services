from typing import Annotated
from fastapi import APIRouter, Depends
from backend.service.api.security import get_current_user
from backend.service.api.services.prediction_service import PredictionService, prediction_service
from backend.service.api.schemas import User

router = APIRouter(
    prefix="/prediction",
    tags=["prediction"]
)


@router.post("/make_prediction")
async def create_prediction(model: str, input_data: str,
                            predict_service: Annotated[PredictionService, Depends(prediction_service)],
                            user: User = Depends(get_current_user)) -> str:
    return await predict_service.get_prediction(user_id=user.id, model=model, input_data=input_data)
