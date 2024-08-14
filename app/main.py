import logging.config
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from app.routes import accounts

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    import httpx

    request_client = httpx.AsyncClient()
    headers = {"Host": "localhost"}
    response = await request_client.get(
        "http://accounts:8000/accounts/api/healthcheck/",
        headers=headers,
    )
    print(response.status_code)
    print("APP STARTING")
    yield
    print("APP STOPPING")


app = FastAPI(lifespan=lifespan)

# Include the router from accounts.py
app.include_router(accounts.router, prefix="/api")


@app.get("/api/healthcheck/")
async def healthcheck():
    return {"status": "Service is up and running"}


logger = logging.getLogger("app")
