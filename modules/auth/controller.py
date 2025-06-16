from http.client import HTTPException
from fastapi import APIRouter
from modules.auth.service import AuthService

router = APIRouter()


@router.post("/login")
def login(username: str, password: str) -> int:
    try:
        return 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/register")
def register(username: str, email: str, password: str) -> bool:
    try:
        return AuthService.create_user(username=username, email=email, password=password
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    