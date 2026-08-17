import logging

from faststream.rabbit import RabbitMessage

from app.broker.publisher import (
    payment_dlq_publisher,
    payment_retry_publisher_1,
    payment_retry_publisher_2,
    payment_retry_publisher_3,
)
from app.dto.payment import PaymentCreatedEvent

logger = logging.getLogger(__name__)


class RetryService:
    MAX_RETRIES = 3

    def __init__(self) -> None:
        pass

    def get_retry_count(
        self,
        message: RabbitMessage,
    ) -> int:

        headers = message.headers or {}

        return int(
            headers.get(
                "x-retry-count",
                0,
            ),
        )

    async def handle_failure(
        self,
        event: PaymentCreatedEvent,
        message: RabbitMessage,
        retry_count: int,
    ) -> None:

        next_retry = retry_count + 1

        headers = dict(
            message.headers or {},
        )

        headers["x-retry-count"] = next_retry

        if next_retry == 1:
            await payment_retry_publisher_1.publish(
                event.model_dump(),
                headers=headers,
            )

        elif next_retry == 2:
            await payment_retry_publisher_2.publish(
                event.model_dump(),
                headers=headers,
            )

        elif next_retry == 3:
            await payment_retry_publisher_3.publish(
                event.model_dump(),
                headers=headers,
            )

        else:
            await payment_dlq_publisher.publish(
                event.model_dump(),
                headers=headers,
            )

            logger.error(
                "Payment %s moved to DLQ",
                event.payment_id,
            )

            await message.ack()

            return

        logger.warning(
            "Payment %s scheduled for retry #%s",
            event.payment_id,
            next_retry,
        )

        await message.ack()
