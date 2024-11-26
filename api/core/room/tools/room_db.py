from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from core.room.models.room import Room
from datetime import datetime
from .members_db import add_user_to_room
from core.room.schemas.room import RoomBase

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

async def get_all_rooms(
    session: AsyncSession
) -> list[Room]:
    result = await session.execute(select(Room))
    rooms = result.scalars().all()

    # Заменяем наличие пароля на булевое значение True/False
    rooms_with_private_status = [
        RoomBase(
            id=room.id,
            is_active=room.is_active,
            opening_time=room.opening_time,
            private=bool(room.password)  # Устанавливаем private в зависимости от наличия пароля
        )
        for room in rooms
    ]

    return rooms_with_private_status