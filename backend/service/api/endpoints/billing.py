from typing import Annotated
from fastapi import APIRouter, Depends

from backend.service.api.schemas import User
from backend.service.api.services.user_service import UserService, user_service
from backend.service.api.security import get_current_user_from_cookie


router = APIRouter(prefix="/billing", tags=["billing"])


@router.get("/balance")
async def get_balance(user_service: Annotated[UserService, Depends(user_service)],
                      current_user: User = Depends(get_current_user_from_cookie)) -> int:
    print(current_user)
    balance = await user_service.get_balance(current_user)
    return balance
