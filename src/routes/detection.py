from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import cv2
from urllib import request
import numpy as np
from datetime import datetime
from ultralytics import YOLO
import re
import easyocr
from skimage.segmentation import clear_border
from sqlalchemy.orm import Session
from typing import Annotated

from src.models.business_license_plate import business_license_plate
from src.models.license_plate import LicensePlate
from src.models.business import Business
from src.config.middlewares.firebase import get_user_token
from src.config.database import db_dependency
from src.proxies.yolo import YOLOModelProxy

model = YOLOModelProxy.get_model()

detections_router = APIRouter()

class HookRequest(BaseModel):
    image_url: str

@detections_router.post("", tags=["Detections"])
async def scan(hook: HookRequest, user: Annotated[dict, Depends(get_user_token)], db: db_dependency):
    try:
        # Fetch and preprocess the image
        url = hook.image_url
        resize_url = url.replace("upload", "upload/w_600/q_100")
        req = request.urlopen(resize_url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Predict
        results = model.predict(img)[0]

        # Extract the bounding boxes and classes
        bboxes = [(x1, y1, x2, y2, score, class_id) for x1, y1, x2, y2, score, class_id in results.boxes.data.tolist()]
        classes = [model.names[int(class_id)] for _, _, _, _, _, class_id in results.boxes.data.tolist()]

        if not bboxes:
            raise HTTPException(status_code=400, detail="No license plate detected")

        # Process the first detected license plate
        x1, y1, x2, y2, _, _ = bboxes[0]
        plate = img[int(y1):int(y2), int(x1):int(x2)]
        plate = cv2.resize(plate, (0, 0), fx=1.5, fy=1.5)
        plate = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
        plate = cv2.threshold(plate, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        plate = cv2.medianBlur(plate, 3)

        # Read text from the plate
        reader = easyocr.Reader(['es'])
        text = reader.readtext(plate)
        if not text:
            raise HTTPException(status_code=400, detail="No text detected on license plate")

        clean_text = re.sub('[^A-Za-z0-9]+', '', text[0][-2]).upper()
        plate_number = clean_text
        
        print("Plate number:", plate_number)

        # Validate plate number
        plate_exists = db.query(LicensePlate).filter(LicensePlate.plate == plate_number).first()
        if not plate_exists:
            raise HTTPException(status_code=404, detail="Plate not found")

        plate_active = db.query(business_license_plate).filter(
            business_license_plate.c.licensePlateId == plate_exists.id,
            business_license_plate.c.checkOut == None
        ).first()
        if not plate_active:
            raise HTTPException(status_code=400, detail="Plate already active or paid")

        # Validate business
        firebaseId = user.get("uid")
        business = db.query(Business).filter(Business.firebaseId == firebaseId).first()
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")

        # Calculate the total to pay
        total_minutes_parked = (datetime.now() - plate_active.createdAt).total_seconds() / 60
        total_to_pay = total_minutes_parked * business.coastPerMinute

        # Update the record
        db.execute(
            business_license_plate.update().values(
                checkOut=datetime.now(),
                updatedAt=datetime.now(),
                minutesParked=total_minutes_parked,
                amount=total_to_pay,
                paid=True
            ).where(
                business_license_plate.c.licensePlateId == plate_exists.id
            )
        )
        
        db.commit()
        
        
        
        return {"result": plate_number, "total_to_pay": total_to_pay}

    except Exception as e:
        print(str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

