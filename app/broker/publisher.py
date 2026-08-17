import logging

from app.broker.broker import broker
from app.broker.topology import (
    PAYMENT_CREATED,
    PAYMENT_DLQ,
    PAYMENT_RETRY_1,
    PAYMENT_RETRY_2,
    PAYMENT_RETRY_3,
    payments_dlx,
    payments_exchange,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


payments_publisher = broker.publisher(
    exchange=payments_exchange,
    routing_key=PAYMENT_CREATED,
)

payment_retry_publisher_1 = broker.publisher(
    exchange=payments_dlx,
    routing_key=PAYMENT_RETRY_1,
)

payment_retry_publisher_2 = broker.publisher(
    exchange=payments_dlx,
    routing_key=PAYMENT_RETRY_2,
)

payment_retry_publisher_3 = broker.publisher(
    exchange=payments_dlx,
    routing_key=PAYMENT_RETRY_3,
)

payment_dlq_publisher = broker.publisher(
    exchange=payments_dlx,
    routing_key=PAYMENT_DLQ,
)


async def publish_payment_created(payload: dict):
    logger.info(f"Publish payment created: {payload}")
    await payments_publisher.publish(payload)
