from fastapi_users import FastAPIUsers
from core.authentication.models.user import User
from core.authentication.tools.user_manager_getter import get_user_manager
from core.authentication.auth.backend import auth_backend

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)