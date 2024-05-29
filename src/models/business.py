from src.config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Uuid
from sqlalchemy.orm import relationship
import datetime

class Business(Base):
    __tablename__ = 'business'
    
    firebaseId = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    owner = Column(String, nullable=False, unique=True)
    coastPerMinute = Column(Integer, nullable=False)
    createdAt = Column(DateTime, nullable=False, default=datetime.datetime.now(datetime.UTC))
    updatedAt = Column(DateTime, nullable=True)
    deletedAt = Column(DateTime, nullable=True)
    licensePlates = relationship("LicensePlate", secondary="business_license_plate", back_populates="businesses")
    deviceId = Column(Uuid, nullable=True)