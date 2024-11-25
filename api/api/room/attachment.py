from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, File as UploadFileType
import os
from api.authentication.fastapi_users import current_active_user

from core.authentication.models.user import User
from core.room.tools.attachment_db import save_file_metadata
from core.db.worker.worker import db_worker

router = APIRouter(
    prefix="/room",
    tags=["Room"],
    dependencies=[Depends(HTTPBearer(auto_error=False))]
)

@router.post("/rooms/{room_id}/upload")
async def upload_file(
    room_id: int,
    file: UploadFile,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_worker.session_getter)
):

    upload_dir = f"uploads/room_{room_id}"
    os.makedirs(upload_dir, exist_ok=True)  # Создает директорию, если ее нет

    # Сохраняем файл на сервере
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Сохраняем метаданные файла в базе данных через сервис
    saved_file = await save_file_metadata(
        session=session,
        room_id=room_id,
        user_id=user.id,
        filename=file.filename,
        path=file_path,
        size=file.file.tell()
    )

    return {"message": "Файл успешно загружен.", "file_id": saved_file.id}