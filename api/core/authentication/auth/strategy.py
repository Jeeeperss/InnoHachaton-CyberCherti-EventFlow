from fastapi import Depends
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy

from core.authentication.models.access_token import AccessToken
from core.authentication.tools.access_token_db import get_access_tokens_db

def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_tokens_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db, 
        lifetime_seconds=3600
        )