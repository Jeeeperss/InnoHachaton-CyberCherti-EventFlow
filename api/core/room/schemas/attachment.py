from pydantic import BaseModel

class AttachmentBase(BaseModel):
    id: int
    room_id: int
    filename: str
    uploaded_by: int