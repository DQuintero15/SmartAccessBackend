import datetime
from sqlalchemy import Column, Integer, Table, ForeignKey, DateTime, Boolean, String, Uuid
from src.config.database import Base




business_license_plate = Table(
    'business_license_plate',
    Base.metadata,
    Column('businessId', String, ForeignKey('business.firebaseId')),
    Column('licensePlateId', Uuid, ForeignKey('license_plate.id')),
    Column('checkInSource', String, nullable=False),
    Column('checkOutSource ', String, nullable=True),
    Column('createdAt', DateTime, default=datetime.datetime.now(datetime.timezone.utc)),
    Column('updatedAt', DateTime),
    Column('deletedAt', DateTime),
    Column('checkOut', DateTime),
    Column('minutesParked', Integer, default=0),
    Column('amount', Integer, default=0),
    Column('paid', Boolean, default=False),
)
