from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.worker.worker import db_worker
from core.room.tools.message_db import add_message
from core.authentication.models.user import User
from .dependencies.connection_manager import manager

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: int,
    db: AsyncSession = Depends(db_worker.session_getter)
):
    # Подключаем пользователя к комнате
    await manager.connect(websocket, room_id)
    try:
        while True:
            # Получаем сообщение от пользователя
            message = await websocket.receive_text()

            # Добавляем сообщение в БД и отправляем его всем пользователям комнаты
            await manager.send_private_message(db, room_id, message)

    except WebSocketDisconnect:
        # Отключение пользователя от комнаты
        await manager.disconnect(websocket, room_id)