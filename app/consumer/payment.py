from faststream import FastStream

from app.broker.broker import broker
from app.broker.topology import payments_exchange, payments_queue

app = FastStream(broker)

@broker.subscriber(
    queue=payments_queue,
    exchange=payments_exchange,
)
async def handle_payment_created(payload: dict):
    print(f"Received payment created: {payload}")
