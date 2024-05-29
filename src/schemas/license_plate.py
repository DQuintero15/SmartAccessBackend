from pydantic import BaseModel

class LicensePlate(BaseModel):
    plate: str
    createdAt: str
    updatedAt: str
    deletedAt: str

