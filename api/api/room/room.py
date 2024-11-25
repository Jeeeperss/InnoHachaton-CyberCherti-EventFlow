from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.authentication.fastapi_users import current_active_user

from core.room.tools.room_db import add_room, get_all_rooms
from core.authentication.models.user import User

from core.db.worker.worker import db_worker
from formatters.time_getter import parse_opening_time
from core.room.schemas.room import RoomBase

from .attachment import router as router_attachment
from .members import router as router_members

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

@router.get("/", response_model=list[RoomBase])
async def all_rooms(
    session: AsyncSession = Depends(db_worker.session_getter)
):
    all_rooms = await get_all_rooms(session)
    return all_rooms

