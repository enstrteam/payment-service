import logging

from app.broker.broker import broker
from app.broker.topology import payments_exchange
from app.dto.payment import PaymentCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



payments_publisher = broker.publisher(
    exchange=payments_exchange,
    routing_key="payment.created",
)

async def publish_payment_created(payload: dict):
    logger.info(f"Publish payment created: {payload}")
    await payments_publisher.publish(payload)
