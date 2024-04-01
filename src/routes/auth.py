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
        user_created = supa.auth.sign_up(credentials={
            "email": sign_up_data.email,
            "password": sign_up_data.password,
            "options": {
                "data": {
                    "first_name": sign_up_data.first_name,
                    "last_name": sign_up_data.last_name,
                    "email_verified": True,
                    "business_name": sign_up_data.business_name.capitalize(),
                    "parking_fee_per_minute": sign_up_data.parking_fee_per_minute,
                }
            }
        })
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
        if e.__class__.__name__ == "AuthApiError":
            return JSONResponse(status_code=401, content=jsonable_encoder({"detail": str(e)}))
        return JSONResponse(status_code=500, content=jsonable_encoder({"detail": str(e)}))
