from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.schemas.business_license_plate import CreateBusinessLicensePlateFromDevice, CreateBusinessLicensePlateFromApp, UpdateBusinessLicensePlate
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.models.license_plate import LicensePlate
from src.models.business_license_plate import business_license_plate
from sqlalchemy import select, exists
from src.models.business import Business

from typing import Annotated
from src.config.middlewares.firebase import get_user_token
from src.config.middlewares.basic import verify_basic_session
from src.config.database import db_dependency
from firebase_admin import messaging
import threading
from datetime import datetime, timezone

def send_notification(plate):
    message = messaging.Message(
        notification=messaging.Notification(
            title="🚗 Nuevo vehículo detectado",
            body=f"Placa: {plate}"
        ),
        topic="new_vehicle_detected"
    )
    messaging.send(message)


plates_router = APIRouter()


@plates_router.post("/camera", status_code= 201)
async def create_plate(auth: Annotated[dict, Depends(verify_basic_session)], db: db_dependency, plate: CreateBusinessLicensePlateFromDevice):

    deviceId = plate.deviceId

    business = db.query(Business).filter(Business.deviceId == deviceId).first()
    
    if not business:
        return JSONResponse(status_code=404, content=jsonable_encoder({"message": "Business not found"}))
    
    plate_exists = db.query(LicensePlate).filter(LicensePlate.plate == plate.plate).first()
    
    if not plate_exists:
        plate_exists = LicensePlate(plate=plate.plate)
        db.add(plate_exists)
        db.commit()
        db.refresh(plate_exists)
        
    # plate_has_already_active = db.query(business_license_plate).filter(business_license_plate.c.licensePlateId == plate_exists.id, business_license_plate.c.checkOut == None).exists()
   
    plate_has_already_active = db.query(
        exists().where(
            (business_license_plate.c.licensePlateId == plate_exists.id) &
            (business_license_plate.c.checkOut == None)
        )
    ).scalar()
    
    if plate_has_already_active:
        return JSONResponse(status_code=400, content=jsonable_encoder({"message": "Plate already active"}))
    
    new_plate = business_license_plate.insert().values(
        businessId=business.firebaseId,
        licensePlateId=plate_exists.id,
        checkInSource=plate.checkInSource,
        minutesParked=0,
        amount=0,
    )
    db.execute(new_plate)
    db.commit()
    

    thread = threading.Thread(target=send_notification, args=(plate.plate,))
    thread.start()
    
    return JSONResponse(status_code=201, content=jsonable_encoder({"message": "Plate created"}))


@plates_router.post("/app", status_code=201)
async def create_plate_from_app(auth: Annotated[dict, Depends(get_user_token)], db: db_dependency, plate: CreateBusinessLicensePlateFromApp):

    firebaseId = auth.get("uid")

    business = db.query(Business).filter(Business.firebaseId == firebaseId).first()
    
    if not business:
        return JSONResponse(status_code=404, content=jsonable_encoder({"message": "Business not found"}))
    
    plate_exists = db.query(LicensePlate).filter(LicensePlate.plate == plate.plate).first()
    
    if not plate_exists:
        plate_exists = LicensePlate(plate=plate.plate)
        db.add(plate_exists)
        db.commit()
        db.refresh(plate_exists)
        
    plate_has_already_active = db.query(
        exists().where(
            (business_license_plate.c.licensePlateId == plate_exists.id) &
            (business_license_plate.c.checkOut == None)
        )
    ).scalar()
    
    if plate_has_already_active:
        return JSONResponse(status_code=400, content=jsonable_encoder({"message": "Plate already active"}))
    
    new_plate = business_license_plate.insert().values(
        businessId=business.firebaseId,
        licensePlateId=plate_exists.id,
        checkInSource=plate.checkInSource,
    )
    db.execute(new_plate)
    db.commit()
    
    return JSONResponse(status_code=201, content=jsonable_encoder({"message": "Plate created"}))


@plates_router.get("", status_code=200)
async def get_plates(auth: Annotated[dict, Depends(get_user_token)], db: db_dependency):
    firebaseId = auth.get("uid")
    
    business = db.query(Business).filter(Business.firebaseId == firebaseId).first()
    
    if not business:
        return JSONResponse(status_code=404, content=jsonable_encoder({"message": "Business not found"}))
    
    plates_query = (
        select(business_license_plate, LicensePlate)
        .join(LicensePlate, business_license_plate.c.licensePlateId == LicensePlate.id)
        .where(business_license_plate.c.businessId == business.firebaseId)
        .where(business_license_plate.c.checkOut != None)
        .order_by(business_license_plate.c.checkInSource.desc())
    )
    plates_result = db.execute(plates_query).fetchall()
    
    plates_dict = [dict(row._mapping) for row in plates_result]
    
    return JSONResponse(status_code=200, content=jsonable_encoder(plates_dict))

@plates_router.get("/non-check-in", status_code=200)
async def get_plates(auth: Annotated[dict, Depends(get_user_token)], db: db_dependency):
    firebaseId = auth.get("uid")
    
    business = db.query(Business).filter(Business.firebaseId == firebaseId).first()
    
    if not business:
        return JSONResponse(status_code=404, content=jsonable_encoder({"message": "Business not found"}))
    
    plates_query = (
        select(business_license_plate, LicensePlate)
        .join(LicensePlate, business_license_plate.c.licensePlateId == LicensePlate.id)
        .where(business_license_plate.c.businessId == business.firebaseId)
        .where(business_license_plate.c.checkOut == None)
        .order_by(business_license_plate.c.checkInSource.desc())
    )
    plates_result = db.execute(plates_query).fetchall()
    
    plates_dict = [dict(row._mapping) for row in plates_result]
    
    return JSONResponse(status_code=200, content=jsonable_encoder(plates_dict))

@plates_router.post("/check-out-app", status_code=200)
async def check_out_plate(auth: Annotated[dict, Depends(get_user_token)], db: db_dependency, plate: UpdateBusinessLicensePlate):
    firebaseId = auth.get("uid")
    
    business = db.query(Business).filter(Business.firebaseId == firebaseId).first()
    
    if not business:
        return JSONResponse(status_code=404, content=jsonable_encoder({"message": "Business not found"}))
    
    plate_exists = db.query(LicensePlate).filter(LicensePlate.plate == plate.plate).first()
    
    if not plate_exists:
        return JSONResponse(status_code=404, content=jsonable_encoder({"message": "Plate not found"}))
    
    plate_active = db.query(business_license_plate).filter(
        business_license_plate.c.licensePlateId == plate_exists.id,
        business_license_plate.c.checkOut == None
    ).first()
    
    if not plate_active:
        return JSONResponse(status_code=400, content=jsonable_encoder({"message": "Plate already active or paid"}))
    
    
    current_utc_date = datetime.now(timezone.utc)
    plate_active_created_at_utc = plate_active.createdAt.replace(tzinfo=timezone.utc)
    total_minutes_parked = (current_utc_date - plate_active_created_at_utc).total_seconds() / 60
    total_to_pay = total_minutes_parked * business.coastPerMinute
    
    db.execute(
        business_license_plate.update().values(
            checkOut=current_utc_date,
            updatedAt=current_utc_date,
            minutesParked=total_minutes_parked,
            amount=total_to_pay,
            paid=True
        ).where(
            business_license_plate.c.licensePlateId == plate_exists.id
        )
    )
    
    db.commit()
    
    return JSONResponse(status_code=200, content=jsonable_encoder({"minutes_parked": total_minutes_parked, "total_to_pay": total_to_pay}))