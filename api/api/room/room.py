from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.authentication.fastapi_users import current_active_user

from core.room.tools.room_db import add_room, get_room_members, add_user_to_room, leave_room
from core.authentication.models.user import User
from core.authentication.schemas.user import UserRead

from core.db.worker.worker import db_worker

from formatters.time_getter import parse_opening_time

router = APIRouter(
    prefix="/room",
    tags=["Room"],
    dependencies=[Depends(HTTPBearer(auto_error=False))]
)

@router.post("/")
async def create_room(
    password: str | None = None, 
    opening_time: str | None = None,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_worker.session_getter)
):
    new_room = await add_room(
        session=session, 
        user_id = user.id, 
        opening_time = parse_opening_time(opening_time), 
        password=password)
    return new_room


@router.get("/{room_id}",  response_model=list[UserRead])
async def get_members(
    room_id: int,
    session: AsyncSession = Depends(db_worker.session_getter)
):
    members = await get_room_members(session=session, room_id=room_id)
    return members

@router.post("/enter/{room_id}")
async def user_to_room(
    room_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_worker.session_getter)
):
    await add_user_to_room(session=session, user_id=user.id, room_id=room_id)
    return {"message": f"Пользователь успешно добавлен в комнату {room_id}."}

@router.delete("/leave/{room_id}")
async def leave_room_route(
    room_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_worker.session_getter)
):
    await leave_room(session=session, user_id=user.id, room_id=room_id)
    return {"detail": f"Пользователь с ID {user.id} успешно вышел из комнаты {room_id}."}