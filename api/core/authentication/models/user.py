from core.db.base.base import Base

from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"  # Обязательно указываем имя таблицы

    id: Mapped[int] = mapped_column(primary_key=True)

    rooms: Mapped[list["Room"]] = relationship(
        back_populates="members",
        secondary="room_user_association"
    )

    attachments: Mapped[list["Attachment"]] = relationship("Attachment", back_populates="user")

    @classmethod
    def get_user_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session, cls)
