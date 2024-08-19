import httpx
from starlette.requests import Request

API_START_POINT = "/api/v1"


def fill_paths(paths: dict, service: str) -> dict:
    new_paths = {}
    for path, value in paths.items():
        new_key = f"{API_START_POINT}/{service}/{path.lstrip('/')}"
        new_paths[new_key] = value

        for method in new_paths[new_key]:
            new_paths[new_key][method].update(security=[{"jwtAuth": []}, {}])

    return new_paths


async def forward_request(request: Request, url: str):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=url,
            headers=request.headers,
            data=await request.body(),
        )
    return response
