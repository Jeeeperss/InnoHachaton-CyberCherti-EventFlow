from core.db.base.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

class Attachment(Base):
    __tablename__ = "attachment"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(nullable=False)  # Имя файла
    path: Mapped[str] = mapped_column(nullable=False)  # URL к файлу
    size: Mapped[int] = mapped_column(nullable=False)  # 

    room_id: Mapped[int] = mapped_column(ForeignKey("room.id", ondelete="CASCADE"), nullable=False)
    uploaded_by: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    room: Mapped["Room"] = relationship(back_populates="attachments")
    user: Mapped["User"] = relationship("User", back_populates="attachments")