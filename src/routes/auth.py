from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from src.config.supabase import supa
from src.schemas.auth import SignUpSchema, SignInSchema

auth_router = APIRouter()

@auth_router.post("/signup", tags=["Authentication"])
async def signup(sign_up_data: SignUpSchema):
    try:
        user_created = supa.auth.sign_up(credentials=sign_up_data.model_dump())
        return JSONResponse(status_code=201, content=jsonable_encoder(user_created))
    
    except RequestValidationError as e:
        return JSONResponse(status_code=400, content=jsonable_encoder({"detail": e.errors()}))
    
    except Exception as e:
        return JSONResponse(status_code=500, content=jsonable_encoder({"detail": str(e)}))

@auth_router.post("/signin", tags=["Authentication"])
async def signin(sign_in_data: SignInSchema):
    try:
        user_signed_in = supa.auth.sign_in_with_password(credentials=sign_in_data.model_dump())
        session = user_signed_in.session
        return JSONResponse(status_code=200, content=jsonable_encoder(session))
    
    except RequestValidationError as e:
        return JSONResponse(status_code=400, content=jsonable_encoder({"detail": e.errors()}))
    
    except Exception as e:
        return JSONResponse(status_code=500, content=jsonable_encoder({"detail": str(e)}))
    
