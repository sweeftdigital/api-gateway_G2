import logging.config
from contextlib import asynccontextmanager

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()


@asynccontextmanager
async def healthcheck(app: FastAPI):
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


app = FastAPI(lifespan=healthcheck)

logger = logging.getLogger("app")


@app.get("/")
async def root():
    logger.debug("Hello World")
    return {"Hello": "World"}
