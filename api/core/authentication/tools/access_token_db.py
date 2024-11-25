from fastapi import Depends

from core.authentication.models.access_token import AccessToken

from sqlalchemy.ext.asyncio import AsyncSession
from core.db.worker.worker import db_worker

async def get_access_tokens_db(
    session: AsyncSession = Depends(db_worker.session_getter),
):
    yield AccessToken.get_db(session=session)