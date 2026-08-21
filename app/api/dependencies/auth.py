import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from app.core.settings import settings

api_key_header = APIKeyHeader(
    name="X-API-Key",
)


async def verify_api_key(
    api_key: Annotated[str | None, Depends(api_key_header)],
) -> None:
    expected_api_key = settings.api_key.get_secret_value()

    if api_key is None or not secrets.compare_digest(
        api_key,
        expected_api_key,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
