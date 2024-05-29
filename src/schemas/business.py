from pydantic import BaseModel

class CreateBusinessSchema(BaseModel):
    name: str
    email: str
    owner: str
    coastPerMinute: int
