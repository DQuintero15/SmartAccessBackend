from pydantic import BaseModel



class UserProfileSchema(BaseModel):
    business_name: str
    email: str
    email_verified: bool
    first_name: str
    last_name: str
    parking_fee_per_minute: int
    phone_verified: bool
    role: str
    sub: str
