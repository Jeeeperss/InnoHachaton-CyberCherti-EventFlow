from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from api.authentication.fastapi_users import fastapi_users
from core.authentication.auth.backend import auth_backend
from core.authentication.schemas.user import UserCreate, UserRead

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[Depends(HTTPBearer(auto_error=False))]
)

router.include_router(
    fastapi_users.get_register_router(
        UserRead, 
        UserCreate
    ) 
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)