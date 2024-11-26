from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
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
            path = path,
            size = size
        )
        session.add(new_file)
        await session.commit()
        await session.refresh(new_file)
        return new_file
    except SQLAlchemyError as e:
        await session.rollback()
        raise e

async def get_all_attachments_of_room(
    session: AsyncSession, 
    room_id: int
) -> list[Attachment]:
    stmt = select(Attachment).where(Attachment.room_id == room_id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_attachment_by_id(session: AsyncSession, attachment_id: int) -> Attachment:
    query = select(Attachment).filter(Attachment.id == attachment_id)
    
    result = await session.execute(query)
    attachment = result.scalar_one_or_none()  # Получаем первую запись или None
    return attachment