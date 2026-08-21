from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.outbox import Outbox, OutboxStatusEnum


class OutboxRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_pending(
        self,
        limit: int = 100,
    ) -> list[Outbox]:
        result = await self.db.execute(
            select(Outbox)
            .where(
                Outbox.status == OutboxStatusEnum.PENDING,
            )
            .order_by(Outbox.created_at)
            .limit(limit),
        )

        return list(result.scalars().all())

    def add(
        self,
        outbox: Outbox,
    ) -> None:
        self.db.add(outbox)
