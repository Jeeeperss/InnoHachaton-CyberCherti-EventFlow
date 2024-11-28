from core.authentication.models.user import User
from core.room.models.room import Room, RoomUserAssociation
from sqlalchemy import select, delete, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from helpers.hasher import check_password
from core.room.models.roles import RoleEnum
import random

async def add_user_to_room(
    session: AsyncSession, 
    user_id: int, 
    room_id: int, 
    role: RoleEnum = RoleEnum.MEMBER,
    password: str = None,
) -> None:
    """
    Добавляет пользователя в комнату, проверяя наличие его в комнате и правильность пароля.
    
    :param session: Асинхронная сессия базы данных.
    :param user_id: ID пользователя, которого нужно добавить.
    :param room_id: ID комнаты, в которую нужно добавить пользователя.
    :param role: Роль пользователя в комнате (по умолчанию MEMBER).
    :param password: Пароль комнаты, если он требуется.
    :raises ValueError: Если пользователь уже в комнате, комната не существует или пароль неверен.
    :raises SQLAlchemyError: Ошибки при работе с базой данных.
    """
    try:
        # Проверка, состоит ли пользователь уже в комнате
        association_result = await session.execute(
            select(RoomUserAssociation)
            .where(RoomUserAssociation.user_id == user_id, RoomUserAssociation.room_id == room_id)
        )
        association = association_result.scalar_one_or_none()
        if association:
            raise ValueError(f"Пользователь с ID {user_id} уже в комнате с ID {room_id}.")

        # Проверка существования комнаты
        room_result = await session.execute(
            select(Room).where(Room.id == room_id)
        )
        room = room_result.scalar_one_or_none()
        if not room:
            raise ValueError(f"Комната с ID {room_id} не существует.")

        if room.password and not check_password(raw_password=password, hashed_password=room.password):
            raise ValueError("Пароль неверен.")

        # Добавление ассоциации пользователя с комнатой
        room_user_association = RoomUserAssociation(
            user_id=user_id, 
            room_id=room_id,
            role=role
        )
        session.add(room_user_association)

        await session.commit()

    except (SQLAlchemyError, ValueError) as e:
        await session.rollback()
        raise e


async def get_room_members(
    session: AsyncSession, 
    room_id: int
) -> list[User]:
    """
    Получает всех пользователей в указанной комнате.

    :param session: Асинхронная сессия базы данных.
    :param room_id: ID комнаты для получения списка пользователей.
    :return: Список пользователей в комнате.
    """
    try:
        result = await session.execute(
            select(User)
            .join(Room.members)
            .where(Room.id == room_id)
        )
        members = result.scalars().all()
        return members
    except SQLAlchemyError as e:
        raise ValueError(f"Ошибка при получении пользователей комнаты с ID {room_id}: {e}")


async def leave_room(session: AsyncSession, user_id: int, room_id: int) -> None:
    """
    Удаляет пользователя из комнаты.
    
    :param session: Асинхронная сессия базы данных.
    :param user_id: ID пользователя, который покидает комнату.
    :param room_id: ID комнаты, которую покидает пользователь.
    :raises ValueError: Если пользователь не состоит в комнате.
    :raises SQLAlchemyError: Ошибки при работе с базой данных.
    """
    try:
        # Проверяем, состоит ли пользователь в комнате
        user_in_room = await session.execute(
            select(RoomUserAssociation)
            .where(RoomUserAssociation.user_id == user_id, RoomUserAssociation.room_id == room_id)
        )
        user_in_room = user_in_room.scalar_one_or_none()

        if not user_in_room:
            raise ValueError(f"Пользователь с ID {user_id} не состоит в комнате с ID {room_id}.")

        role = user_in_room.role

        # Если пользователь не является владельцем
        if role != RoleEnum.OWNER:
            # Удаляем ассоциацию пользователя с комнатой
            await session.execute(
                delete(RoomUserAssociation)
                .where(RoomUserAssociation.user_id == user_id, RoomUserAssociation.room_id == room_id)
            )
            await session.commit()
            return f"Пользователь {user_id} успешно покинул комнату {room_id}."

        # Если пользователь является владельцем
        # Считаем количество участников
        count_result = await session.execute(
            select(func.count(RoomUserAssociation.user_id))
            .where(RoomUserAssociation.room_id == room_id)
        )
        user_count = count_result.scalar()

        # Если он единственный участник — удалить комнату
        if user_count == 1:
            await session.execute(
                delete(Room)
                .where(Room.id == room_id)
            )
            await session.commit()
            return f"Пользователь {user_id} покинул комнату {room_id}, комната удалена."

        # Если участников больше одного — передать роль владельца
        other_users = await session.execute(
            select(RoomUserAssociation)
            .where(RoomUserAssociation.room_id == room_id, RoomUserAssociation.user_id != user_id)
        )
        other_users = other_users.scalars().all()

        # Выбираем случайного участника
        new_owner = random.choice(other_users)
        new_owner.role = RoleEnum.OWNER

        # Удаляем текущего владельца из комнаты
        await session.execute(
            delete(RoomUserAssociation)
            .where(RoomUserAssociation.user_id == user_id, RoomUserAssociation.room_id == room_id)
        )

        await session.commit()
        return f"Пользователь {user_id} покинул комнату {room_id}, новый владелец: {new_owner.user_id}."

    except Exception as e:
        await session.rollback()
        raise e
