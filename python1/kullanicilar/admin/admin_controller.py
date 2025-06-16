from fastapi import APIRouter, Depends, HTTPException
from kullanicilar.service.auth_service.auth_service import get_current_kullanici
from kullanicilar.model.model import kullaniciInDB

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/panel")
def read_admin_panel(current_kullanici: kullaniciInDB = Depends(get_current_kullanici)):
    # Admin kontrolü
    if not current_kullanici.is_admin:
        raise HTTPException(status_code=403, detail="Admin yetkisi gerekli")
    
    return {
        "message": f"Hoş geldin {current_kullanici.name}! Bu admin panelidir.",
        "email": current_kullanici.email,
    }