from pydantic import BaseModel

from enum import Enum

class Role(str, Enum):
    admin = "admin"
    user = "user"

class SignUpSchema(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    business_name: str
    parking_fee_per_minute: float
    role: Role = Role.admin
    

class SignInSchema(BaseModel):
    email: str
    password: str
    