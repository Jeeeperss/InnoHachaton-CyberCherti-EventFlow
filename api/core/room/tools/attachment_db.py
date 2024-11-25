from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from core.room.models.attachment import Attachment

async def save_file_metadata(
    session: AsyncSession, 
    room_id: int, 
    user_id: int, 
    filename: str, 
    path: str, 
    size: int
) -> Attachment:
    try:
        new_file = Attachment(
            room_id = room_id,
            uploaded_by = user_id,
            filename = filename,
            path = filename,
            size = size
        )
        session.add(new_file)
        await session.commit()
        await session.refresh(new_file)
        return new_file
    except SQLAlchemyError as e:
        await session.rollback()
        raise e