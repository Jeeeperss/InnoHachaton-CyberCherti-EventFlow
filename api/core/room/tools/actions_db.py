from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from core.room.models.room import RoomUserAssociation
from core.room.models.roles import RoleEnum

async def kick_user_from_room(
    session: AsyncSession, 
    room_id: int, 
    owner_id: int, 
    user_id_to_kick: int
    ) -> None:
    """
    Исключает пользователя из комнаты. Только владелец комнаты может исключить пользователя.
    
    :param session: Сессия базы данных
    :param room_id: ID комнаты
    :param owner_id: ID владельца комнаты
    :param user_id_to_kick: ID пользователя, которого нужно исключить
    """
    # Проверяем, является ли пользователь владельцем комнаты
    if not await is_owner(session, room_id, owner_id):
        raise PermissionError("Только владелец комнаты может исключить пользователей.")
    
    # Находим ассоциацию между пользователем и комнатой
    result = await session.execute(
        select(RoomUserAssociation)
        .where(RoomUserAssociation.room_id == room_id, RoomUserAssociation.user_id == user_id_to_kick)
    )
    association = result.scalar_one_or_none()
    
    if not association:
        raise ValueError(f"Пользователь с ID {user_id_to_kick} не найден в комнате с ID {room_id}.")
    
    # Удаляем ассоциацию (пользователь исключён из комнаты)
    await session.execute(
        delete(RoomUserAssociation)
        .where(RoomUserAssociation.room_id == room_id, RoomUserAssociation.user_id == user_id_to_kick)
    )
    
    # Сохраняем изменения в базе данных
    await session.commit()

async def is_owner(session: AsyncSession, room_id: int, user_id: int) -> bool:
    """
    Проверка, является ли пользователь владельцем комнаты.

    :param session: Сессия базы данных
    :param room_id: ID комнаты
    :param user_id: ID пользователя
    :return: True, если пользователь — владелец, иначе False
    """
    result = await session.execute(
        select(RoomUserAssociation.role)
        .where(RoomUserAssociation.room_id == room_id, RoomUserAssociation.user_id == user_id)
    )
    role = result.scalar_one_or_none()
    return role == RoleEnum.OWNER
