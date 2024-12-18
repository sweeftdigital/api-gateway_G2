import asyncio
import json
from contextlib import asynccontextmanager

import httpx
import websockets
import yaml
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.websockets import WebSocket, WebSocketDisconnect

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
    request_client = httpx.AsyncClient()

    for service, url in MICROSERVICES.items():
        response = await request_client.get(url=f"https://{url}/schema/")
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

    yield {"aclient": request_client}


app = FastAPI(lifespan=get_service_schema)
origins = [
    "*",
    "http://localhost:3000",
    "https://rev-front-dev-g2-424868328181.europe-west3.run.app/",
    "https://reverse-auction-front-g2-424868328181.europe-west3.run.app/",
    "https://rev-front-dev-g2-424868328181.europe-west3.run.app",
    "https://reverse-auction-front-g2-424868328181.europe-west3.run.app",
    "https://admin-g2-424868328181.europe-west3.run.app/",
    "https://admin-g2-dev-424868328181.europe-west3.run.app/",
    "https://admin-g2-424868328181.europe-west3.run.app",
    "https://admin-g2-dev-424868328181.europe-west3.run.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.route(
    path="/{service}/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def route_to_microservice(request: Request):
    service = request.path_params.get("service")
    path = request.path_params.get("path")

    if service not in MICROSERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    service_url = f"https://{MICROSERVICES.get(service)}/{path}"
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


@app.websocket("/{service}/{path:path}")
async def websocket_route_to_microservice(
    websocket: WebSocket, service: str, path: str
):
    if service not in MICROSERVICES:
        await websocket.close(code=1003)  # Invalid service
        return

    service_url = f"wss://{MICROSERVICES.get(service)}/{path}"
    if websocket.query_params:
        service_url += f"?{websocket.query_params}"

    # Extract headers from the client connection
    headers = dict(websocket.headers)

    # Create extra_headers for the microservice connection
    extra_headers = {
        k: v
        for k, v in headers.items()
        if k.lower() in ["authorization", "cookie", "x-api-key", "accept-language"]
    }

    await websocket.accept()

    try:
        async with websockets.connect(
            service_url,
            extra_headers=extra_headers,
            timeout=10,
        ) as microservice_ws:

            async def forward_to_service():
                try:
                    async for message in websocket.iter_text():
                        await microservice_ws.send(message)
                except WebSocketDisconnect:
                    pass

            async def forward_to_client():
                try:
                    async for message in microservice_ws:
                        await websocket.send_text(message)
                except websockets.ConnectionClosed:
                    pass

            await asyncio.gather(
                forward_to_service(),
                forward_to_client(),
            )

    except websockets.exceptions.WebSocketException as e:
        print(f"WebSocket error: {e}")
    except asyncio.TimeoutError:
        print("Connection to microservice timed out.")
        await websocket.close(code=1006)
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        try:
            # Check if the connection is still open using the client_state
            if websocket.client_state.CONNECTED:
                await websocket.close()
        except RuntimeError:
            # Handle case where connection is already closed
            pass
