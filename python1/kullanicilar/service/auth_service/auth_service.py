from passlib.context import CryptContext
from kullanicilar.db.db import fake_kullanici_db
from kullanicilar.model.model import kullaniciInDB
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

# Şifreleme sistemi (bcrypt ile)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT ayarları
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Swagger için manuel token girişi (Bearer token)
security = HTTPBearer()

# 🔐 Şifre kontrolü (kullanıcı girişinde kullanılır)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 🧑 Kullanıcı kimlik doğrulaması
def authenticate_kullanici(email: str, password: str) -> Optional[kullaniciInDB]:
    kullanici = fake_kullanici_db.get(email)
    if not kullanici:
        return None
    if not verify_password(password, kullanici.hashed_password):
        return None
    return kullanici

# 🔑 JWT Token üretimi
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
"""
# 🔒 Token doğrulama ve kullanıcıyı çözümleme (Manuel token girişi için)
def get_current_kullanici(credentials: HTTPAuthorizationCredentials = Depends(security)) -> kullaniciInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Geçersiz kimlik doğrulama bilgisi",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Token'ı al (Bearer prefix'i otomatik olarak kaldırılır)
        token = credentials.credentials
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("sub") # JWT içinde "sub": email olmalı
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    kullanici = fake_kullanici_db.get(email)
    if kullanici is None:
        raise credentials_exception
    return kullanici
"""
def get_current_kullanici(credentials: HTTPAuthorizationCredentials = Depends(security)) -> kullaniciInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Geçersiz kimlik doğrulama bilgisi",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        print(f"🔍 Temiz token: {token[:30]}...")
        
        # Bearer prefix'i zaten HTTPBearer tarafından kaldırılmış olmalı
        # Ama emin olmak için kontrol edelim
        if token.startswith("bearer "):
            token = token[7:]  # "bearer " kısmını kaldır
            print(f"🔍 Bearer kaldırıldı: {token[:30]}...")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"🔍 Payload: {payload}")
        
        email = payload.get("sub")
        print(f"🔍 JWT'den email: '{email}'")
        print(f"🔍 DB keyleri: {list(fake_kullanici_db.keys())}")
        
        if email is None:
            raise credentials_exception
            
    except JWTError as e:
        print(f"❌ JWT Error: {e}")
        raise credentials_exception

    kullanici = fake_kullanici_db.get(email)
    print(f"🔍 Bulunan kullanıcı: {kullanici}")
    
    if kullanici is None:
        raise credentials_exception
    return kullanici