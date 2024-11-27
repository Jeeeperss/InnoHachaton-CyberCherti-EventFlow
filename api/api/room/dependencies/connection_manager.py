from fastapi import WebSocket
import json
from core.room.tools.message_db import add_message


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}  # Храним подключения по user_id
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Принимаем подключение и сохраняем его в active_connections."""
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def disconnect(self, websocket: WebSocket):
        """При отключении удаляем пользователя из списка активных соединений."""
        for user_id, connection in self.active_connections.items():
            if connection == websocket:
                del self.active_connections[user_id]
                break

    async def send_message(self, message: str, websocket: WebSocket):
        """Отправка сообщения конкретному пользователю."""
        await websocket.send_text(message)

    async def send_private_message(self, session, room_id: str, user_id: int, message: str):
        """Отправка приватного сообщения между пользователями в рамках комнаты."""
        #message_data = json.loads(message)
        #room_id = message_data['room_id']
        #sender_id = message_data['sender_id']
        #receiver_id = message_data['receiver_id']  # ID получателя
        #content = message_data['content']

        # Добавление сообщения в БД
        await add_message(
            session=session,
            room_id=int(room_id),
            sender_id=user_id,
            content=message
        )

        # Получаем сокет получателя по ID
        receiver_socket = self.active_connections.get(receiver_id)

        # Если сокет получателя найден, отправляем сообщение
        if receiver_socket:
            await receiver_socket.send_text(f"Message from {sender_id}: {content}")


# Инициализация менеджера
manager = ConnectionManager()
