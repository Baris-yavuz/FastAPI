from pydantic import BaseModel

class kullanici(BaseModel):
    id: int
    name: str
    email: str

class kullaniciInDB(kullanici):
    hashed_password: str
    is_admin: bool = False  # Varsayılan olarak admin değil

