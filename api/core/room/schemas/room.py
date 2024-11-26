from pydantic import BaseModel
from datetime import datetime

class RoomBase(BaseModel):
    id: int
    is_active: bool
    opening_time: datetime
    private: bool