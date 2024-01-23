from fastapi import APIRouter

from backend.service.api.endpoints.auth import router as auth_endpoint
from backend.service.api.endpoints.billing import router as billing_endpoint
from backend.service.api.endpoints.predictions import router as predictions_endpoint


routers = [auth_endpoint, billing_endpoint, predictions_endpoint]

api_router = APIRouter(prefix="/api")

for router in routers:
    api_router.include_router(router)
