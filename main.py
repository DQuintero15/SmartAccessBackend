
from fastapi import FastAPI
from src.routes.profile import profile_router
from src.routes.auth import auth_router
from src.routes.hook import hook_router

app = FastAPI(title="SmartAccess API", version="0.1.0", summary="API for SmartAccess")

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(profile_router, prefix="/profile", tags=["Profile"])
app.include_router(hook_router, prefix="/hook", tags=["Hook"])

@app.get("/", tags=["root"])
def read_root():
    return {"message": "SmartAccess API is running!"}
