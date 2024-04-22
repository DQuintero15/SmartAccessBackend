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
                    "role": sign_up_data.role
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

@auth_router.post("/refresh", tags=["Authentication"])
async def refresh_token():
    try:
        new_session = supa.auth.refresh_session()
        return JSONResponse(status_code=200, content=jsonable_encoder(new_session))
    
    except RequestValidationError as e:
        return JSONResponse(status_code=400, content=jsonable_encoder({"detail": e.errors()}))
    
    except Exception as e:
        if e.__class__.__name__ == "AuthApiError":
            return JSONResponse(status_code=401, content=jsonable_encoder({"detail": str(e)}))
        return JSONResponse(status_code=500, content=jsonable_encoder({"detail": str(e)}))
    
@auth_router.post("/retrive-new-session", tags=["Authentication"])
async def retrive_new_session():
    try:
        new_session = supa.auth.set_session("eyJhbGciOiJIUzI1NiIsImtpZCI6Ijd4Mk9COWxPeE1MalBIWGgiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzEyMTQ1MzUxLCJpYXQiOjE3MTIxNDE3NTEsImlzcyI6Imh0dHBzOi8vZWFha2ZpZHBha3RqZnhhcXpmeWIuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6IjUyMGJiNzI2LTkxYjEtNDZjYy1iNjBhLTMwYTg4ZDJiM2U4NCIsImVtYWlsIjoicXVpbnRlcm9kMTY0QGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiYnVzaW5lc3NfbmFtZSI6IkF1dG8gb2FzaXMiLCJlbWFpbCI6InF1aW50ZXJvZDE2NEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcnN0X25hbWUiOiJKb2huIiwibGFzdF9uYW1lIjoiRG9lIiwicGFya2luZ19mZWVfcGVyX21pbnV0ZSI6OTcsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwicm9sZSI6ImFkbWluIiwic3ViIjoiNTIwYmI3MjYtOTFiMS00NmNjLWI2MGEtMzBhODhkMmIzZTg0In0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3MTIxNDE3NTF9XSwic2Vzc2lvbl9pZCI6IjFhZmVjOGNiLTRmMDUtNGZlMC1iZGUzLTM1MGQ1N2IxYjNhZSIsImlzX2Fub255bW91cyI6ZmFsc2V9.F5TbQco9KKPnfiuwie_wmjXATH3QKk2aqnfwpIEKyXo",
                                            "LtNfHO5x3nsb7SJ0QilSmQ")
        return JSONResponse(status_code=200, content=jsonable_encoder(new_session))
    
    except RequestValidationError as e:
        return JSONResponse(status_code=400, content=jsonable_encoder({"detail": e.errors()}))
    
    except Exception as e:
        if e.__class__.__name__ == "AuthApiError":
            return JSONResponse(status_code=401, content=jsonable_encoder({"detail": str(e)}))
        return JSONResponse(status_code=500, content=jsonable_encoder({"detail": str(e)}))