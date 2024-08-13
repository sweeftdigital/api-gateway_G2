import logging.config
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
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

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@app.post("/api/login")
async def login(request: UserLogin):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://accounts:8000/accounts/api/token/",
            json=request.dict()
        )
        return response.json()

@app.get("/api/healthcheck/")
async def healthcheck():
    return {"status": "Service is up and running"}

logger = logging.getLogger("app")
