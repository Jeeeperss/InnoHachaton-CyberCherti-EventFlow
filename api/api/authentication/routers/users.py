from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from api.authentication.fastapi_users import fastapi_users

from core.authentication.schemas.user import (
    UserRead,
    UserUpdate,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(HTTPBearer(auto_error=False))]
)

router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)