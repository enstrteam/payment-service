import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dto.payment import PaymentCreate, PaymentResponse
from app.models.outbox import Outbox
from app.models.payment import Payment


class PaymentService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_payment(self, payment: PaymentCreate, idempotency_key: str) -> PaymentResponse:

        existing_result = await self._get_payment_by_idempotency_key(idempotency_key)

        if existing_result is not None:
            return PaymentResponse.model_validate(existing_result)

        payment = Payment(
            amount=payment.amount,
            currency=payment.currency,
            webhook_url=payment.webhook_url,
            idempotency_key=idempotency_key,
            description=payment.description,
            meta=payment.meta,
        )
        self.db.add(payment)

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

        self.db.add(outbox)
        await self.db.commit()
        await self.db.refresh(payment)
        return PaymentResponse.model_validate(payment)

    async def get_payment(self, payment_id: uuid.UUID) -> PaymentResponse:
        payment = await self.db.get(Payment, payment_id)
        if payment is None:
            raise HTTPException(
                status_code=404,
                detail="Payment not found",
            )
        return PaymentResponse.model_validate(payment)  


    async def _get_payment_by_idempotency_key(self, idempotency_key: str) -> PaymentResponse:
        result = await self.db.execute(
            select(Payment).where(
                Payment.idempotency_key == idempotency_key
            )
        )

        return result.scalar_one_or_none()
