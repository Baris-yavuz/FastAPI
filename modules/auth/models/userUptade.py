from pydantic import BaseModel

class UserUpdate(BaseModel):
    email: str
