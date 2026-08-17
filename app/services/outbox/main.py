import asyncio

from app.broker.broker import broker
from app.services.outbox.worker import run_outbox_worker


async def main():
    async with broker:
        await run_outbox_worker()


if __name__ == "__main__":
    asyncio.run(main())
