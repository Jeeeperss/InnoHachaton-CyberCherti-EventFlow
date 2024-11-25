from fastapi import Depends
from core.authentication.auth.user_manager import UserManager
from .user_db import get_user_db

async def get_user_manager(user_db = Depends(get_user_db)):
    yield UserManager(user_db)