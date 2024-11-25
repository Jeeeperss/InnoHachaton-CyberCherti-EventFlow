from fastapi import Depends

from core.authentication.models.user import User

from sqlalchemy.ext.asyncio import AsyncSession
from core.db.worker.worker import db_worker

async def get_user_db(
    session: AsyncSession = Depends(db_worker.session_getter),
):
    yield User.get_user_db(session=session)