import logging.config

from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("APP STARTING")
    yield
    print("APP STOPPING")


app = FastAPI(lifespan=lifespan)

logger = logging.getLogger("app")


@app.get("/")
async def root():
    logger.debug("Hello World")
    return {"Hello": "World"}
