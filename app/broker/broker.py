from faststream.rabbit import RabbitBroker

from app.core.settings import settings

broker = RabbitBroker(
    settings.rabbitmq_settings.amqp_url.unicode_string(),
)
