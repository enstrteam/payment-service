from fastapi import APIRouter

from app.api.routes.payment import router as payment_router

router = APIRouter()

router.include_router(payment_router, prefix="/payments", tags=["payments"])


@router.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "healthy"}
