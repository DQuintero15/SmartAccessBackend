from src.config.database import Base
from sqlalchemy import Column, String, DateTime, UUID
from sqlalchemy.orm import relationship
import datetime
import uuid


class LicensePlate(Base):
    __tablename__ = 'license_plate'
    
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    plate = Column(String, nullable=False, unique=True)
    createdAt = Column(DateTime, nullable=False, default=datetime.datetime.now(datetime.UTC))
    updatedAt = Column(DateTime, nullable=True)
    deletedAt = Column(DateTime, nullable=True)
    businesses = relationship("Business", secondary="business_license_plate", back_populates="licensePlates")