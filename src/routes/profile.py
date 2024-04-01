from fastapi import APIRouter, Depends
from src.config.supabase import supa
from src.security.JwtBearer import JWTBearer


profile_router = APIRouter()

@profile_router.get("", tags=["Profile"], dependencies = [Depends(JWTBearer())])
async def get_profile():
    return supa.auth.get_user()