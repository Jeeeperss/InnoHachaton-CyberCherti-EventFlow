from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.room.models.message import Message
from sqlalchemy.exc import SQLAlchemyError

async def add_message(
    session: AsyncSession,
    sender_id: int, 
    room_id: int, 
    content: str,
) -> Message:
    """
    Добавляем новое сообщение в базу данных.
    :param session: Асинхронная сессия базы данных.
    :param sender_id: Идентификатор отправителя
    :param room_id: ID комнаты, к которой привязано сообщение.
    :param content: Содержимое сообщения
    :return: Созданное сообщение
    """
    try:
        new_message = Message(
            room_id=room_id,
            sender_id = sender_id,
            content = content
        )
        session.add(new_message)
        await session.commit()
        await session.refresh(new_message)
        return new_message
    except SQLAlchemyError as e:
        # Откат транзакции в случае ошибки
        await session.rollback()
        raise Exception(f"Ошибка при сохранении метаданных файла: {str(e)}")


async def get_messages_in_room(
    session: AsyncSession,
    room_id: int,
    limit: int = None  # Если None, то лимита не будет
) -> list[Message]:
    """
    Получаем все сообщения из комнаты по ID, с возможностью указания лимита.
    :param session: Асинхронная сессия базы данных.
    :param room_id: ID комнаты, для которой нужно получить сообщения.
    :param limit: Максимальное количество сообщений для извлечения. Если None, то ограничений нет.
    :return: Список сообщений
    """
    try:
        # Запрос к базе данных для получения сообщений из указанной комнаты
        query = select(Message).where(Message.room_id == room_id)
        
        # Если limit не None, добавляем ограничение
        if limit is not None:
            query = query.limit(limit)

        # Сортировка по ID
        query = query.order_by(Message.id.asc())
        
        # Выполняем запрос
        result = await session.execute(query)
        messages = result.scalars().all()
        return messages
    except SQLAlchemyError as e:
        raise Exception(f"Ошибка при получении сообщений из комнаты: {str(e)}")
