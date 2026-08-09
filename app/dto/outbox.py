import uuid
from datetime import datetime

from app.dto.base import BaseSchema
from app.models.enum import OutboxStatusEnum


class OutboxCreate(BaseSchema):
    aggregate_id: uuid.UUID
    event_type: str
    payload: dict
    status: OutboxStatusEnum
    attempts: int = 0
    published_at: datetime | None = None


class OutboxResponse(BaseSchema):
    id: uuid.UUID
    aggregate_id: uuid.UUID
    event_type: str
    payload: dict
    status: OutboxStatusEnum
    attempts: int
    published_at: datetime | None = None
