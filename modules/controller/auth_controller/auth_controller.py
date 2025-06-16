from fastapi import APIRouter, HTTPException
from modules.model.model import LoginRequest
from modules.service.auth_service.auth_service import authenticate_kullanici, create_access_token
from datetime import timedelta

router = APIRouter()

@router.post("/login")
def login(request: LoginRequest):
    kullanici = authenticate_kullanici(request.email, request.password)
    if not kullanici:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(
        data={"sub": kullanici.email},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}
