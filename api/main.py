from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.authentication.routers.auth import router as router_auth
from api.authentication.routers.users import router as router_user
from api.room.room import router as router_room
from api.room.attachment import router as router_attachment
# Создаем экземпляр FastAPI
app = FastAPI()

# Определяем разрешенные источники для CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://127.0.0.1"
]

# Добавляем middleware для обработки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешенные источники
    allow_credentials=True,   # Разрешить отправку учетных данных
    allow_methods=["*"],      # Разрешить все HTTP-методы
    allow_headers=["*"],      # Разрешить все заголовки
)

app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_room)
app.include_router(router_attachment)