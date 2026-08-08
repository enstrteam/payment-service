from datetime import datetime
from decimal import Decimal

from sqlalchemy import JSON, DateTime, Enum, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.enum import CurrencyEnum, PaymentStatusEnum


class Payment(Base):
    __tablename__ = "payments"
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[CurrencyEnum] = mapped_column(
        Enum(CurrencyEnum), nullable=False, default=CurrencyEnum.RUB
    )
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    meta: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[PaymentStatusEnum] = mapped_column(
        Enum(PaymentStatusEnum), nullable=False, default=PaymentStatusEnum.PENDING
    )
    idempotency_key: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    webhook_url: Mapped[str] = mapped_column(String, nullable=False)
    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
