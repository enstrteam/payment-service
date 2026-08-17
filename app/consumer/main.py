from faststream import FastStream
from faststream.middlewares.acknowledgement.config import AckPolicy
from faststream.rabbit import RabbitMessage

from app.broker.broker import broker
from app.broker.setup import setup_rabbit_topology
from app.broker.topology import (
    payments_exchange,
    payments_queue,
)
from app.consumer.payment.consumer import PaymentConsumer
from app.core.dependencies.faststream_database import DatabaseSession
from app.dto.payment import PaymentCreatedEvent

app = FastStream(broker)


@app.after_startup
async def setup_topology() -> None:
    await setup_rabbit_topology()


@broker.subscriber(
    queue=payments_queue,
    exchange=payments_exchange,
    ack_policy=AckPolicy.MANUAL,
)
async def handle_payment_created(
    event: PaymentCreatedEvent,
    message: RabbitMessage,
    db: DatabaseSession,
) -> None:

    consumer = PaymentConsumer(db)

    await consumer.handle(
        event=event,
        message=message,
    )
