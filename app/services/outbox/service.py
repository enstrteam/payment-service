import logging
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.broker.publisher import publish_payment_created
from app.core.dependencies.database import DatabaseSession
from app.dto.outbox import OutboxResponse
from app.models.outbox import Outbox, OutboxStatusEnum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OutboxService:
    def __init__(self, db: AsyncSession = DatabaseSession):
        self.db = db

    async def publish(self) -> None:

        result: OutboxResponse = await self.db.execute(
            select(Outbox)
            .where(
                Outbox.status == OutboxStatusEnum.PENDING
            )
            .order_by(Outbox.created_at)
            .limit(100)
        )

        outbox_events: list[OutboxResponse] = result.scalars().all()

        for outbox_event in outbox_events:
            try:
                logger.info(f"Outbox worker published {outbox_event} event")
                await publish_payment_created(outbox_event.payload)

                outbox_event.status = OutboxStatusEnum.PUBLISHED
                outbox_event.published_at = datetime.now(UTC)
            except Exception:
                outbox_event.attempts += 1

        await self.db.commit()
