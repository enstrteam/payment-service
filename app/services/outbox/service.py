import logging
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.broker.publisher import publish_payment_created
from app.models.outbox import OutboxStatusEnum
from app.repositories.outbox import OutboxRepository

logger = logging.getLogger(__name__)


class OutboxService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = OutboxRepository(db)

    async def publish(self) -> None:

        outbox_events = await self.repository.get_pending(limit=100)

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
