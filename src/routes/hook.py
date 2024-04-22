from fastapi import APIRouter, Request

hook_router = APIRouter()

@hook_router.post("", tags=["Hook"])
async def scan(request: Request):
    print(await request.json())