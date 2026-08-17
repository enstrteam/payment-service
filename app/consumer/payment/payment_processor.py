import asyncio
import logging
import random
from datetime import UTC, datetime

from sqlalchemy import select

from app.core.dependencies.faststream_database import DatabaseSession
from app.dto.payment import PaymentCreatedEvent
from app.models.payment import Payment, PaymentStatusEnum

logger = logging.getLogger(__name__)


class PaymentProcessor:
    def __init__(self, db: DatabaseSession) -> None:
        self.db = db

    async def _emulate_payment_processing(
        self,
        payment: Payment,
    ) -> Payment:
        await asyncio.sleep(
            random.uniform(2, 5),
        )

        if random.random() < 0.9:
            payment.status = PaymentStatusEnum.SUCCEEDED
        else:
            payment.status = PaymentStatusEnum.FAILED

        payment.processed_at = datetime.now(UTC)

        return payment

    async def get_payment(
        self,
        payment_id,
    ) -> Payment:
        result = await self.db.execute(
            select(Payment).where(
                Payment.id == payment_id,
            ),
        )

        payment = result.scalar_one_or_none()

        if payment is None:
            raise ValueError(
                f"Payment {payment_id} not found",
            )

        return payment

    async def process_payment(
        self,
        event: PaymentCreatedEvent,
    ) -> Payment:
        payment = await self.get_payment(event.payment_id)

        if payment.status != PaymentStatusEnum.PENDING:
            logger.info(
                "Payment %s already processed: status=%s",
                payment.id,
                payment.status,
            )

            return payment

        logger.info(
            "Processing payment %s",
            payment.id,
        )

        payment = await self._emulate_payment_processing(payment)

        logger.info(
            "Payment %s processed: status=%s",
            payment.id,
            payment.status,
        )

        await self.db.commit()

        return payment
