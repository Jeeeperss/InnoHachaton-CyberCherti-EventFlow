from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse
from api.authentication.fastapi_users import current_active_user
from core.db.worker.worker import db_worker
from core.room.tools.message_db import add_message
from core.authentication.models.user import User
from .dependencies.connection_manager import manager

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

@router.websocket("/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: int, db: AsyncSession = Depends(db_worker.session_getter)):
    # Подключаем пользователя к комнате
    await manager.connect(websocket, user_id)

    try:
        while True:
            # Получаем сообщение от пользователя
            message = await websocket.receive_text()
            
            # Логика для отправки сообщений в комнату
            await manager.send_private_message(db, room_id, user_id, message)

    except WebSocketDisconnect:
        # Отключение пользователя
        await manager.disconnect(websocket)
        print(f"User {user_id} disconnected from room {room_id}")


