from fastapi import WebSocket
from typing import Dict, List
from core.room.tools.message_db import add_message
import json

class ConnectionManager:
    def __init__(self):
        self.active_rooms: Dict[int, List[WebSocket]] = {}  # Храним подключения по room_id

    async def connect(self, websocket: WebSocket, room_id: int):
        """Принимаем подключение и сохраняем его в active_rooms."""
        await websocket.accept()
        if room_id not in self.active_rooms:
            self.active_rooms[room_id] = []
        self.active_rooms[room_id].append(websocket)

    async def disconnect(self, websocket: WebSocket, room_id: int):
        """Удаляем пользователя из активных соединений комнаты."""
        if room_id in self.active_rooms:
            if websocket in self.active_rooms[room_id]:
                self.active_rooms[room_id].remove(websocket)
            # Удаляем комнату, если она пуста
            if not self.active_rooms[room_id]:
                del self.active_rooms[room_id]

    async def send_message_to_room(self, room_id: int, message: str):
        """Отправка сообщения всем пользователям комнаты."""
        connections = self.active_rooms.get(room_id, [])
        for connection in connections:
            await connection.send_text(message)

    async def send_private_message(self, session, room_id: int, message: str):
        """Отправка сообщения в комнату с добавлением в БД."""
        message_data = json.loads(message) 
        content = message_data['content']
        sender_id = message_data['sender_id']
        await add_message(
            session=session,
            room_id=room_id,
            sender_id=sender_id,
            content=content
        )

        # Отправляем сообщение всем участникам комнаты
        await self.send_message_to_room(
            room_id=room_id,
            message=f"{sender_id} : {content}"
        )


# Инициализация менеджера
manager = ConnectionManager()
