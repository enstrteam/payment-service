from faststream.rabbit import ExchangeType, RabbitExchange, RabbitQueue

payments_exchange = RabbitExchange(
    name="payments",
    type=ExchangeType.TOPIC,
    durable=True,
)
payments_queue = RabbitQueue(
    name="payments.new",
    durable=True,
    routing_key="payment.created",
)
