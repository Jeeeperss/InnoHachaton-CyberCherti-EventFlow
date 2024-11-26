from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.authentication.fastapi_users import current_active_user
from core.db.worker.worker import db_worker
from core.authentication.models.user import User
from core.room.tools.actions_db import kick_user_from_room

router = APIRouter(
    prefix="/actions",
    tags=["Actions"],
    dependencies=[Depends(HTTPBearer(auto_error=False))]
)

@router.delete("/{room_id}/users/{user_id_to_kick}")
async def kick_member(
    room_id: int,
    user_id_to_kick: int,
    owner: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_worker.session_getter)
):
    await kick_user_from_room(
        session, 
        room_id=room_id, 
        owner_id=owner.id, 
        user_id_to_kick=user_id_to_kick
    )
    return {"message": f"Пользователь {user_id_to_kick} исключен из комнаты {room_id}"}