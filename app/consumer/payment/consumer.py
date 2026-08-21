import logging

from faststream.rabbit import RabbitMessage
from sqlalchemy.ext.asyncio import AsyncSession

from app.consumer.payment.payment_processor import PaymentProcessor
from app.consumer.payment.retry_service import RetryService
from app.consumer.payment.webhook_service import WebhookService
from app.dto.payment import PaymentCreatedEvent
from app.repositories.payment import PaymentRepository

logger = logging.getLogger(__name__)


class PaymentConsumer:
    def __init__(self, db: AsyncSession) -> None:
        repository = PaymentRepository(db)
        self.payment_processor = PaymentProcessor(repository, db)
        self.webhook_service = WebhookService()
        self.retry_service = RetryService()

    async def handle(
        self,
        event: PaymentCreatedEvent,
        message: RabbitMessage,
    ) -> None:

        retry_count = self.retry_service.get_retry_count(message)

        try:
            payment = await self.payment_processor.process_payment(
                event,
            )

            await self.webhook_service.send(payment)

        except Exception:
            logger.exception(
                "Payment %s failed",
                event.payment_id,
            )

            await self.retry_service.handle_failure(
                event=event,
                message=message,
                retry_count=retry_count,
            )

            return

        await message.ack()

        logger.info(
            "Payment %s completed successfully",
            event.payment_id,
        )
