import os

import httpx
from fastapi import APIRouter, HTTPException, status

from app.schemas.accounts_schemas import TokenRefresh, UserLogin

router = APIRouter()

BASE_URL = (
    f"http://{os.getenv('ACCOUNTS_API_HOST')}:"
    f"{os.getenv('ACCOUNT_SERVICE_PORT')}/accounts/api"
)


@router.post("/login")
async def login(request: UserLogin):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/token/", json=request.model_dump()
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Error from the token service.",
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Error communicating with the token service.",
            )


@router.post("/token/refresh")
async def refresh_token(request: TokenRefresh):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/token/refresh/",
                json=request.model_dump(),
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Error from the token service.",
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Error communicating with the token service.",
            )
