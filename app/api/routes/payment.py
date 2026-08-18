import uuid

from fastapi import APIRouter, Header

from app.api.services.payment import PaymentService
from app.core.dependencies.database import DatabaseSession
from app.dto.payment import PaymentCreate, PaymentResponse

router = APIRouter()


@router.post("",status_code=202, tags=["payments"])
async def create_payment(
    payment: PaymentCreate,
    db: DatabaseSession,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
) -> PaymentResponse:
    payment_service = PaymentService(db)
    return await payment_service.create_payment(payment, idempotency_key)


@router.get("/{payment_id}", tags=["payments"])
async def get_payment(
    payment_id: uuid.UUID,
    db: DatabaseSession,
) -> PaymentResponse:
    payment_service = PaymentService(db)
    return await payment_service.get_payment(payment_id)
