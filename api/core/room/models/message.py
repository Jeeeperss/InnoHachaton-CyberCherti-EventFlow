from core.db.base.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)  # Имя файла

    room_id: Mapped[int] = mapped_column(ForeignKey("room.id", ondelete="CASCADE"), nullable=False)
    sender_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    room: Mapped["Room"] = relationship(back_populates="messages")
    user: Mapped["User"] = relationship("User", back_populates="messages")