from faststream.rabbit import ExchangeType, RabbitExchange, RabbitQueue

PAYMENT_CREATED = "payment.created"

PAYMENT_RETRY_1 = "payment.retry.1"
PAYMENT_RETRY_2 = "payment.retry.2"
PAYMENT_RETRY_3 = "payment.retry.3"

PAYMENT_DLQ = "payment.dlq"


payments_exchange = RabbitExchange(
    name="payments",
    type=ExchangeType.DIRECT,
    durable=True,
)
payments_queue = RabbitQueue(
    name="payments.new",
    durable=True,
    routing_key=PAYMENT_CREATED,
)


payments_dlx = RabbitExchange(
    name="payments.dlx",
    type=ExchangeType.DIRECT,
    durable=True,
)


payment_retry_queue_1 = RabbitQueue(
    name="payments.retry.1",
    durable=True,
    routing_key=PAYMENT_RETRY_1,
    arguments={
        "x-message-ttl": 2000,
        "x-dead-letter-exchange": payments_exchange.name,
        "x-dead-letter-routing-key": PAYMENT_CREATED,
    },
)

payment_retry_queue_2 = RabbitQueue(
    name="payments.retry.2",
    durable=True,
    routing_key=PAYMENT_RETRY_2,
    arguments={
        "x-message-ttl": 4000,
        "x-dead-letter-exchange": payments_exchange.name,
        "x-dead-letter-routing-key": PAYMENT_CREATED,
    },
)

payment_retry_queue_3 = RabbitQueue(
    name="payments.retry.3",
    durable=True,
    routing_key=PAYMENT_RETRY_3,
    arguments={
        "x-message-ttl": 8000,
        "x-dead-letter-exchange": payments_exchange.name,
        "x-dead-letter-routing-key": PAYMENT_CREATED,
    },
)


payment_dlq_queue = RabbitQueue(
    name="payments.dlq",
    durable=True,
    routing_key=PAYMENT_DLQ,
)
