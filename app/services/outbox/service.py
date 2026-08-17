import logging
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.broker.publisher import publish_payment_created
from app.models.outbox import Outbox, OutboxStatusEnum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OutboxService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def publish(self) -> None:

        result = await self.db.execute(
            select(Outbox)
            .where(
                Outbox.status == OutboxStatusEnum.PENDING
            )
            .order_by(Outbox.created_at)
            .limit(100)
        )

        outbox_events: list[Outbox] = result.scalars().all()

        for outbox_event in outbox_events:
            try:
                logger.info(f"Outbox worker published {outbox_event} event")
                await publish_payment_created(outbox_event.payload)

                outbox_event.status = OutboxStatusEnum.PUBLISHED
                outbox_event.published_at = datetime.now(UTC)
            except Exception:
                logger.exception(
                    "Failed to publish outbox event %s",
                    outbox_event.id,
                )
                outbox_event.attempts += 1

        await self.db.commit()
