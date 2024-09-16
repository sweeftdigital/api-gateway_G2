import json
from contextlib import asynccontextmanager

import httpx
import yaml
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from .config import MICROSERVICES
from .helpers import fill_paths, forward_request

load_dotenv()


@asynccontextmanager
async def get_service_schema(app: FastAPI):
    app.openapi_schema = get_openapi(
        title="API Gateway",
        version="3.0.3",
        summary="Exposed API for all microservices",
        routes=app.routes,
    )

    async with httpx.AsyncClient() as client:
        for service, url in MICROSERVICES.items():
            response = await client.request(method="GET", url=f"http://{url}/schema/")
            yaml_content = response.content.decode("utf-8")

            json_data = yaml.safe_load(yaml_content)
            schemas = json_data.get("components").get("schemas")
            security = json_data.get("components").get("securitySchemes")

            paths = json_data.get("paths")
            paths = fill_paths(paths, service)

            app.openapi_schema["paths"].update(paths)
            if not app.openapi_schema.get("components"):
                app.openapi_schema["components"] = {}
                app.openapi_schema["components"]["schemas"] = {}

            if json_data.get("components").get("securitySchemes"):
                app.openapi_schema["components"]["securitySchemes"] = {}
                app.openapi_schema["components"]["securitySchemes"].update(security)

            app.openapi_schema["components"]["schemas"].update(schemas)

    yield


app = FastAPI(lifespan=get_service_schema)
templates = Jinja2Templates(directory="app/templates")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.route(  # noqa
    path="/{service}/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def route_to_microservice(request: Request):
    service = request.path_params.get("service")
    path = request.path_params.get("path")

    if service not in MICROSERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    service_url = f"http://{MICROSERVICES.get(service)}/{path}"
    response = await forward_request(request, service_url)

    content_type = response.headers.get("content-type")
    status_code = response.status_code
    if content_type and "text/html" in content_type:
        return HTMLResponse(content=response.content, status_code=response.status_code)

    if status_code == 204 or not response.content:
        return Response(status_code=status_code)

    return JSONResponse(
        content=json.loads(response.content), status_code=response.status_code
    )


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"swagger_url": "/docs"}
    )
