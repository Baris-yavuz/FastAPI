from fastapi import APIRouter
from modules.service.service import get_all_kullanicilar, get_kullanici_id
from modules.service.auth_service.auth_service import authenticate_kullanici, create_access_token
from modules.service.auth_service.auth_service import timedelta
from modules.model.model import LoginRequest
from modules.controller.auth_controller.auth_controller import HTTPException

router = APIRouter() 

@router.get("/")
def read_kullanicilar():
    return  get_all_kullanicilar()

@router.get("/{kullanici_id}")
def read_kullanici(kullanici_id: int):
    return get_kullanici_id(kullanici_id)

@router.post("/login")
def login(request: LoginRequest):
    kullanici = authenticate_kullanici(request.email, request.password)
    if not kullanici:
        raise HTTPException(status_code=401, detail="Geçersiz isim ya da şifre")
    
    access_token = create_access_token(
        data={"sub": kullanici.email},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

