import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.payment import PaymentCreate, PaymentResponse
from app.models.payment import Payment


class PaymentService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_payment(self, payment: PaymentCreate, idempotency_key: str) -> PaymentResponse:
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
