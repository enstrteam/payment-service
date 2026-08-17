from app.broker.broker import broker
from app.broker.topology import (
    PAYMENT_DLQ,
    PAYMENT_RETRY_1,
    PAYMENT_RETRY_2,
    PAYMENT_RETRY_3,
    payment_dlq_queue,
    payment_retry_queue_1,
    payment_retry_queue_2,
    payment_retry_queue_3,
    payments_dlx,
)


async def setup_rabbit_topology() -> None:
    dlx = await broker.declare_exchange(
        payments_dlx,
    )

    retry_queue_1 = await broker.declare_queue(
        payment_retry_queue_1,
    )

    retry_queue_2 = await broker.declare_queue(
        payment_retry_queue_2,
    )

    retry_queue_3 = await broker.declare_queue(
        payment_retry_queue_3,
    )

    dlq_queue = await broker.declare_queue(
        payment_dlq_queue,
    )

    await retry_queue_1.bind(
        dlx,
        routing_key=PAYMENT_RETRY_1,
    )

    await retry_queue_2.bind(
        dlx,
        routing_key=PAYMENT_RETRY_2,
    )

    await retry_queue_3.bind(
        dlx,
        routing_key=PAYMENT_RETRY_3,
    )

    await dlq_queue.bind(
        dlx,
        routing_key=PAYMENT_DLQ,
    )
