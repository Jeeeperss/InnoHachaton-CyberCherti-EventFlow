from sqlalchemy import select, delete

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from core.room.models.room import Room, RoomUserAssociation
from core.authentication.models.user import User

from datetime import datetime

async def add_user_to_room(
    session: AsyncSession, 
    user_id: int, 
    room_id: int
) -> None:
    """Добавить пользователя в комнату."""
    try:
        association_result = await session.execute(
            select(RoomUserAssociation)
            .where(RoomUserAssociation.user_id == user_id, RoomUserAssociation.room_id == room_id)
        )
        association = association_result.scalar_one_or_none()
        if association:
            raise ValueError(f"Пользователь с id {user_id} уже в комнате с id {room_id}.")

        room_user_association = RoomUserAssociation(
            user_id=user_id, 
            room_id=room_id
        )
        session.add(room_user_association)

        # Сохраняем изменения
        await session.commit()

    except (SQLAlchemyError, ValueError) as e:
        await session.rollback()
        raise e

async def add_room(
    session: AsyncSession, 
    user_id: int, 
    password: str | None, 
    opening_time: datetime | None,
    ) -> Room:
    try:
        is_active = opening_time is None or datetime.utcnow() > opening_time
        new_room = Room(
            is_active = is_active,
            password = password,
            opening_time = opening_time
        )

        session.add(new_room)
        await session.flush()
        await add_user_to_room(
            session = session,
            user_id=user_id,
            room_id=new_room.id
        )

        await session.refresh(new_room)

        return new_room
    except SQLAlchemyError as e:
        await session.rollback()
        raise e

async def get_room_members(
    session: AsyncSession, 
    room_id: int
) -> list[User]:
    """Получить список участников комнаты."""
    result = await session.execute(
        select(User)
        .join(Room.members)  # Используем связь через relationship
        .where(Room.id == room_id)
    )
    members = result.scalars().all()
    return members


async def leave_room(session: AsyncSession, user_id: int, room_id: int) -> None:
    try:
        # Проверяем, состоит ли пользователь в комнате
        user_in_room = await session.execute(
            select(RoomUserAssociation)
            .where(RoomUserAssociation.user_id == user_id, RoomUserAssociation.room_id == room_id)
        )
        if not user_in_room.scalar_one_or_none():
            raise ValueError(f"Пользователь с ID {user_id} не состоит в комнате с ID {room_id}.")

        # Удаляем запись из таблицы RoomUserAssociation
        await session.execute(
            delete(RoomUserAssociation)
            .where(RoomUserAssociation.user_id == user_id, RoomUserAssociation.room_id == room_id)
        )

        # Сохраняем изменения
        await session.commit()
    except (SQLAlchemyError, ValueError) as e:
        await session.rollback()
        raise e
