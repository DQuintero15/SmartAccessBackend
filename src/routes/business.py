from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from src.schemas.business import CreateBusinessSchema
from src.models.business import Business
from src.config.middlewares.firebase import get_user_token
from src.config.database import db_dependency

from typing import Annotated


business_router = APIRouter()

@business_router.post("", status_code=201)
async def create(user: Annotated[dict, Depends(get_user_token)], db: db_dependency, business: CreateBusinessSchema):
    firebaseId = user.get("uid")
    
    if not firebaseId:
        return JSONResponse(status_code=401, content=jsonable_encoder({"message": "User not found"}))
    
    new_business = Business(
        name=business.name,
        email=business.email,
        owner=business.owner,
        coastPerMinute=business.coastPerMinute,
        firebaseId=firebaseId
    )
    
    db.add(new_business)
    db.commit()
    db.refresh(new_business)
    
    return new_business

@business_router.get("", status_code=200)
async def get_one(user: Annotated[dict, Depends(get_user_token)], db: db_dependency):
    firebaseId = user.get("uid")
    
    if not firebaseId:
        return JSONResponse(status_code=401, content=jsonable_encoder({"message": "User not found"}))
    
    business = db.query(Business).filter(Business.firebaseId == firebaseId).first()
    
    return business
