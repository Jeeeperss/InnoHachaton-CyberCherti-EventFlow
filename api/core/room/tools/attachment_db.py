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
    """
    Сохраняет метаданные загруженного файла в базу данных.
    
    :param session: Асинхронная сессия базы данных.
    :param room_id: ID комнаты, к которой привязан файл.
    :param user_id: ID пользователя, который загрузил файл.
    :param filename: Имя загруженного файла.
    :param path: Путь к файлу на сервере.
    :param size: Размер файла в байтах.
    :return: Объект Attachment с сохраненными данными.
    """
    try:
        new_file = Attachment(
            room_id=room_id,
            uploaded_by=user_id,
            filename=filename,
            path=path,
            size=size
        )
        session.add(new_file)
        await session.commit()
        await session.refresh(new_file)
        return new_file
    except SQLAlchemyError as e:
        # Откат транзакции в случае ошибки
        await session.rollback()
        raise Exception(f"Ошибка при сохранении метаданных файла: {str(e)}")


async def get_all_attachments_of_room(
    session: AsyncSession, 
    room_id: int
) -> list[Attachment]:
    """
    Получает все прикрепленные файлы для указанной комнаты.
    
    :param session: Асинхронная сессия базы данных.
    :param room_id: ID комнаты, для которой ищем файлы.
    :return: Список объектов Attachment.
    """
    stmt = select(Attachment).where(Attachment.room_id == room_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_attachment_by_id(
    session: AsyncSession, 
    attachment_id: int
) -> Attachment:
    """
    Получает файл по его ID.
    
    :param session: Асинхронная сессия базы данных.
    :param attachment_id: ID файла, который нужно получить.
    :return: Объект Attachment или None, если файл не найден.
    """
    query = select(Attachment).filter(Attachment.id == attachment_id)
    result = await session.execute(query)
    attachment = result.scalar_one_or_none()
    return attachment
