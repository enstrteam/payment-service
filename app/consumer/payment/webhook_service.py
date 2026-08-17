import logging

import httpx

from app.models.payment import Payment

logger = logging.getLogger(__name__)


class WebhookService:
    async def send(
        self,
        payment: Payment,
    ) -> None:

        payload = {
            "payment_id": str(payment.id),
            "status": payment.status.value,
        }

        timeout = httpx.Timeout(
            connect=5.0,
            read=10.0,
            write=10.0,
            pool=5.0,
        )

        async with httpx.AsyncClient(
            timeout=timeout,
        ) as client:
            response = await client.post(
                payment.webhook_url,
                json=payload,
            )

            response.raise_for_status()

        logger.info(
            "Webhook sent: payment=%s",
            payment.id,
        )
