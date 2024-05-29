from pydantic import BaseModel
from enum import Enum

class SourceType(str, Enum):
    CAMERA = 'CAMERA'
    MANUAL = 'MANUAL'

class BusinessLicensePlate(BaseModel):
    businessId: str
    licensePlateId: str
    checkInSource: SourceType
    checkOutSource: SourceType
    createdAt: str
    updatedAt: str
    deletedAt: str
    checkOut: str
    minutesParked: int
    amount: int
    paid: bool

class CreateBusinessLicensePlateFromDevice(BaseModel):
    plate: str
    checkInSource: SourceType
    deviceId: str
    
class CreateBusinessLicensePlateFromApp(BaseModel):
    plate: str
    checkInSource: SourceType

class UpdateBusinessLicensePlate(BaseModel):
    plate: str

