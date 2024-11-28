from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.worker.worker import db_worker
from core.room.tools.message_db import get_messages_in_room
from .dependencies.genarate_image import generate

router = APIRouter(
    prefix="/image",
    tags=["Image Generateion"],
)

@router.get("/generate")
async def generate_img(
    room_id: int,
    session: AsyncSession = Depends(db_worker.session_getter)
):
    messages = await get_messages_in_room(session=session, room_id=room_id, limit = 10)
    content = " ".join([message.content for message in messages])
    await generate(content, room_id)
    return {"message": f"Изображение сгенерировано на основе текста {content}"}