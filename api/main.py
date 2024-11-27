from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.authentication.routers.auth import router as router_auth
from api.authentication.routers.users import router as router_user

from api.room.room import router as router_room
from api.room.attachment import router as router_attachment
from api.room.members import router as router_members
from api.room.actions import router as router_actions
from api.room.websocket import router as router_websocket

from allowed_origins import origins

# Создаем экземпляр FastAPI
app = FastAPI()

# Добавляем middleware для обработки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins.allowed_origins,  # Разрешенные источники
    allow_credentials=True,   # Разрешить отправку учетных данных
    allow_methods=["*"],      # Разрешить все HTTP-методы
    allow_headers=["*"],      # Разрешить все заголовки
)

app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_room)
app.include_router(router_attachment)
app.include_router(router_members)
app.include_router(router_actions)
app.include_router(router_websocket)