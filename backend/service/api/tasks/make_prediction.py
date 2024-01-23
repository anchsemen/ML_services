import asyncio

from celery import Celery

from backend.service.api.repositories.prediction_repo import PredictionRepository
from backend.service.api.repositories.user_repo import UserRepository
from backend.service.api.tasks.utils import load_model, load_vectorizer

celery = Celery("prediction_tasks", broker="redis://localhost:6379")


@celery.task
def run_model(prediction_id, model_filename, user_id, user_balance, input_data):
    try:
        model = load_model(model_filename)
        vectorizer = load_vectorizer()
        input_data = vectorizer.transform([input_data])
        result = model.predict(input_data)
        data_to_update = {"is_success": True,
                          "is_finished": True,
                          "output_data": result[0][0]}

    except Exception as e:
        print(e)

        asyncio.run(UserRepository().update(data={"balance": user_balance}, id=user_id))

        data_to_update = {"is_success": False,
                          "is_finished": True,
                          "error_info": str(e)}

    asyncio.run(PredictionRepository().update(data=data_to_update, id=prediction_id))
