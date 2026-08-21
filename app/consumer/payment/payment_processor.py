import asyncio
import logging
import random
from datetime import UTC, datetime

from app.core.dependencies.faststream_database import DatabaseSession
from app.dto.payment import PaymentCreatedEvent
from app.models.payment import Payment, PaymentStatusEnum
from app.repositories.payment import PaymentRepository

logger = logging.getLogger(__name__)


class PaymentProcessor:
    def __init__(self, repository: PaymentRepository, db: DatabaseSession) -> None:
        self.repository = repository
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

    async def process_payment(
        self,
        event: PaymentCreatedEvent,
    ) -> Payment:
        payment = await self.repository.get_by_id(event.payment_id)

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
