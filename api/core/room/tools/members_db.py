from core.authentication.models.user import User
from core.room.models.room import Room, RoomUserAssociation
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

async def add_user_to_room(
    session: AsyncSession, 
    user_id: int, 
    room_id: int
) -> None:
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

async def get_room_members(
    session: AsyncSession, 
    room_id: int
) -> list[User]:
    result = await session.execute(
        select(User)
        .join(Room.members)
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
