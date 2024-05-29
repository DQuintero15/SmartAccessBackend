from src.config.settings import get_settings
from src.config.database import  engine
from src.models import business, license_plate, business_license_plate
from src.routes.detection import detections_router
from src.routes.business import business_router
from src.routes.plates import plates_router

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import threading
from ultralytics import YOLO


import firebase_admin
from firebase_admin import credentials


cred = credentials.Certificate(get_settings().firebase_credential_path)
firebase_admin.initialize_app(cred)

app = FastAPI(title="SmartAccess API", version="0.1.0", summary="API for SmartAccess")



business.Base.metadata.create_all(bind=engine)
license_plate.Base.metadata.create_all(bind=engine)
business_license_plate.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(detections_router, prefix="/detections", tags=["Detections"])
app.include_router(business_router, prefix="/businesses", tags=["Businesses"])
app.include_router(plates_router, prefix="/plates", tags=["Vehicle Plates"])

@app.get("/", tags=["root"])
def read_root():
    return {"message": "SmartAccess API is running!"}
