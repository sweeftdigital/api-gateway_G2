import httpx
from fastapi import APIRouter, HTTPException, status

from app.schemas.accounts_schemas import TokenRefresh, UserLogin

router = APIRouter()


@router.post("/login")
async def login(request: UserLogin):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://accounts:8000/accounts/api/token/", json=request.model_dump()
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
                "http://accounts:8000/accounts/api/token/refresh/",
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
