from pydantic import BaseModel

class SignUpSchema(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    business_name: str
    parking_fee_per_minute: float
    

class SignInSchema(BaseModel):
    email: str
    password: str
    