import os

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, File as UploadFileType
from api.authentication.fastapi_users import current_active_user
from fastapi.responses import FileResponse

from core.authentication.models.user import User
from core.room.tools.attachment_db import save_file_metadata, get_all_attachments_of_room, get_attachment_by_id
from core.db.worker.worker import db_worker
from core.room.schemas.attachment import AttachmentBase

router = APIRouter(
    prefix="/attachment",
    tags=["Attachment"],
    dependencies=[Depends(HTTPBearer(auto_error=False))]
)

@router.post("/{room_id}/upload")
async def upload_attachment(
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



@router.get("/{room_id}/all", response_model=list[AttachmentBase])
async def all_attachment(
    room_id: int,
    session: AsyncSession = Depends(db_worker.session_getter)
): 
    attachments = await get_all_attachments_of_room(session=session, room_id=room_id)
    return attachments

@router.get("/download/{attachment_id}", response_class=FileResponse)
async def download_attachment(
    attachment_id: int,
    session: AsyncSession = Depends(db_worker.session_getter)
):
    # Получаем вложение из базы данных
    attachment = await get_attachment_by_id(session, attachment_id)

    # Путь к файлу, который мы вернем пользователю для скачивания
    return FileResponse(
        path=attachment.path,  # путь на сервере
        filename=attachment.filename,  # имя файла, которое будет использоваться при скачивании
        media_type="application/octet-stream"  # тип содержимого для бинарных файлов
    )