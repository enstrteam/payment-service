import uuid
from datetime import datetime
from decimal import Decimal

from app.dto.base import BaseSchema
from app.models.enum import CurrencyEnum, PaymentStatusEnum


class PaymentCreate(BaseSchema):
    amount: Decimal
    currency: CurrencyEnum
    webhook_url: str

    description: str | None = None
    meta: dict | None = None


class PaymentResponse(BaseSchema):
    id: uuid.UUID
    amount: Decimal
    currency: CurrencyEnum
    webhook_url: str
    idempotency_key: str

    description: str | None = None
    meta: dict | None = None

    status: PaymentStatusEnum
    created_at: datetime
    processed_at: datetime | None = None


class PaymentCreatedEvent(BaseSchema):
    payment_id: uuid.UUID
    amount: Decimal
    currency: CurrencyEnum
    webhook_url: str

    description: str | None = None
    meta: dict | None = None
