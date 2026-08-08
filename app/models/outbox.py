import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, Enum, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.enum import OutboxStatusEnum


class Outbox(Base):
    __tablename__ = "outbox"

    aggregate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True)

    event_type: Mapped[str] = mapped_column(String(100), nullable=False)

    payload: Mapped[dict] = mapped_column(JSON, nullable=False)

    status: Mapped[OutboxStatusEnum] = mapped_column(
        Enum(OutboxStatusEnum), nullable=False, default=OutboxStatusEnum.PENDING)

    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True)
