import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.payment import PaymentCreate, PaymentResponse
from app.models.outbox import Outbox
from app.models.payment import Payment
from app.repositories.outbox import OutboxRepository
from app.repositories.payment import PaymentRepository


class PaymentService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.payment_repository = PaymentRepository(db)
        self.outbox_repository = OutboxRepository(db)

    async def create_payment(
        self,
        payment_data: PaymentCreate,
        idempotency_key: str,
    ) -> PaymentResponse:

        existing_payment = await self.payment_repository.get_by_idempotency_key(
            idempotency_key,
        )

        if existing_payment is not None:
            return PaymentResponse.model_validate(
                existing_payment,
            )

        payment = Payment(
            amount=payment_data.amount,
            currency=payment_data.currency,
            webhook_url=payment_data.webhook_url,
            idempotency_key=idempotency_key,
            description=payment_data.description,
            meta=payment_data.meta,
        )

        self.payment_repository.add(payment)

        await self.db.flush()

        event_payload = {
            "payment_id": str(payment.id),
            "amount": str(payment.amount),
            "currency": payment.currency.value,
            "description": payment.description,
            "meta": payment.meta,
            "webhook_url": payment.webhook_url,
        }

        outbox = Outbox(
            aggregate_id=payment.id,
            event_type="payment.created",
            payload=event_payload,
        )

        self.outbox_repository.add(outbox)

        await self.db.commit()
        await self.db.refresh(payment)

        return PaymentResponse.model_validate(payment)

    async def get_payment(
        self,
        payment_id: uuid.UUID,
    ) -> PaymentResponse:

        payment = await self.payment_repository.get_by_id(
            payment_id,
        )

        if payment is None:
            raise HTTPException(
                status_code=404,
                detail="Payment not found",
            )

        return PaymentResponse.model_validate(payment)
