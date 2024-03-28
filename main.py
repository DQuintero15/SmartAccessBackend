
from fastapi import FastAPI
from src.routes.auth import auth_router

app = FastAPI(title="SmartAccess API", version="0.1.0", summary="API for SmartAccess")

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/", tags=["root"])
def read_root():
    return {"message": "SmartAccess API is running!"}
