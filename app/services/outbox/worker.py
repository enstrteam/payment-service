import asyncio
import logging

from app.core.database import database
from app.services.outbox.service import OutboxService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_outbox_worker() -> None:
    logger.info("Outbox worker started")
    while True:
        try:
            logger.info("Outbox worker running")
            async with database.session() as db:
                service = OutboxService(db)

                await service.publish()

        except Exception:
            logger.exception("Outbox worker error")

        await asyncio.sleep(1)
