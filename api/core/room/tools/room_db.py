from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from core.room.models.room import Room, RoomUserAssociation
from datetime import datetime
from .members_db import add_user_to_room
from core.room.schemas.room import RoomBase
from core.room.models.roles import RoleEnum
from helpers.hasher import hash_password

async def create_room(
    session: AsyncSession, 
    user_id: int, 
    password: str | None, 
    opening_time: datetime | None,
) -> Room:
    """
    Создает новую комнату и назначает пользователя владельцем.
    
    :param session: Асинхронная сессия базы данных.
    :param user_id: ID пользователя, создающего комнату.
    :param password: Пароль для комнаты (если None, комната без пароля).
    :param opening_time: Время открытия комнаты (если None, комната активна сразу).
    :return: Объект новой комнаты.
    :raises SQLAlchemyError: Ошибки при работе с базой данных.
    """
    try:
        # Определяем активна ли комната
        is_active = opening_time is None or datetime.utcnow() > opening_time
        hashed_password = hash_password(password) if password else None

        # Создаем объект новой комнаты
        new_room = Room(
            is_active=is_active,
            password=hashed_password,
            opening_time=opening_time
        )

        session.add(new_room)
        await session.flush()

        # Добавляем пользователя как владельца комнаты
        await add_user_to_room(
            session=session,
            user_id=user_id,
            room_id=new_room.id,
            role=RoleEnum.OWNER,
            password=password,
        )

        # Обновляем информацию о комнате
        await session.refresh(new_room)

        return new_room
    except SQLAlchemyError as e:
        await session.rollback()
        raise e


async def get_all_rooms(
    session: AsyncSession
) -> list[RoomBase]:
    """
    Получает список всех комнат с указанием их приватности.
    
    :param session: Асинхронная сессия базы данных.
    :return: Список объектов комнат с информацией о приватности.
    :raises SQLAlchemyError: Ошибки при работе с базой данных.
    """
    result = await session.execute(select(Room))
    rooms = result.scalars().all()

    return [
        RoomBase(
            id=room.id,
            is_active=room.is_active,
            opening_time=room.opening_time,
            private=bool(room.password)  # Если есть пароль, комната приватная
        )
        for room in rooms
    ]


async def delete_room(
    session: AsyncSession, 
    user_id: int, 
    room_id: int
) -> None:
    """
    Удаляет комнату, если пользователь является её владельцем.
    
    :param session: Асинхронная сессия базы данных.
    :param user_id: ID пользователя, который пытается удалить комнату.
    :param room_id: ID комнаты, которую нужно удалить.
    :raises ValueError: Если комната или пользователь не найдены.
    :raises PermissionError: Если пользователь не является владельцем комнаты.
    :raises SQLAlchemyError: Ошибки при работе с базой данных.
    """
    try:
        # Проверяем существование комнаты
        room_query = await session.execute(select(Room).where(Room.id == room_id))
        room = room_query.scalar_one_or_none()

        if not room:
            raise ValueError(f"Комната с id {room_id} не найдена.")

        # Проверяем, является ли пользователь владельцем комнаты
        association_query = await session.execute(
            select(RoomUserAssociation)
            .where(RoomUserAssociation.room_id == room_id, RoomUserAssociation.user_id == user_id)
        )
        association = association_query.scalar_one_or_none()

        if not association:
            raise ValueError(f"Пользователь с id {user_id} не состоит в комнате с id {room_id}.")

        if association.role != RoleEnum.OWNER:
            raise PermissionError(f"Пользователь с id {user_id} не является владельцем комнаты с id {room_id}.")

        # Удаляем комнату и связанные с ней данные
        await session.execute(delete(Room).where(Room.id == room_id))

        # Сохраняем изменения
        await session.commit()

    except Exception as e:
        await session.rollback()
        raise e
