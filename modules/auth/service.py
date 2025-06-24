from modules.auth.models.userCreate import UserCreate
from modules.db.service import DBService, settings
from modules.auth.models.loginRequest import UserLogin
import hashlib
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from modules.auth.models.userUptade import UserUpdate
from pymongo import ReturnDocument


security = HTTPBearer()
ALGORITHM = "HS256"

class AuthService:
    @staticmethod
    def create_user(username: str, email: str, password: str) -> bool:
        try:
            AuthService.check_username(username)
            AuthService.check_email(email)
            password_hash = AuthService.hash_password(password)

            user_id = DBService.get_next_user_id() 

            DBService.auth.insert_one({
                
                    "user_id": user_id,
                    "username":username,
                    "email":email,
                    "hashed_password":password_hash,
                    "role": "user"
            })
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
        
    @staticmethod
    def create_admin(username: str, email: str, password: str) -> bool:
        try:
            AuthService.check_admin_username(username)
            AuthService.check_admin_email(email)
            password_hash = AuthService.hash_password(password)

            admin_id = DBService.get_next_admin_id()

            DBService.admin.insert_one({
                "admin_id": admin_id,
                "username": username,
                "email": email,
                "hashed_password": password_hash,
                "role": "admin"
            })
            return True
        except Exception as e:
            print(f"Error creating admin: {e}")
            return False

    @staticmethod
    def check_admin_username(username: str) -> None:
        admin = DBService.admin.find_one({"username": username})
        if admin is not None:
            raise Exception("Admin kullanıcı adı zaten bulunuyor.")

    @staticmethod
    def check_admin_email(email: str) -> None:
        admin_mail = DBService.admin.find_one({"email": email})
        if admin_mail is not None:
            raise Exception("Admin email adresi zaten bulunuyor.")

    @staticmethod
    def login_admin(username: str, password: str) -> bool:
        try:
            admin_data = DBService.admin.find_one({"username": username})
            if not admin_data:
                print("Admin bulunamadı.")
                return False
            
            password_hash = AuthService.hash_password(password)
            if password_hash != admin_data["hashed_password"]:
                print("Yanlış şifre")
                return False
            
            print("Admin girişi başarılı.")
            return True
        except Exception as e:
            print(f"Hata: {e}")
            return False

    @staticmethod
    def create_admin_token(username: str, admin_id):
        payload = {
            "sub": str(admin_id),
            "username": username,
            "role": "admin",
            "exp": datetime.utcnow() + timedelta(hours=2) 
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
        return token

    @staticmethod
    def get_current_admin(token: HTTPAuthorizationCredentials = Depends(security)):
        try:
            payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[ALGORITHM])
            admin_id = payload.get("sub")
            username = payload.get("username")
            role = payload.get("role")
            
            if admin_id is None or username is None or role != "admin":
                raise HTTPException(status_code=403, detail="Admin yetkisi gerekli")
            return {"admin_id": int(admin_id), "username": username, "role": role}
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token süresi dolmuş")
        except JWTError:
            raise HTTPException(status_code=401, detail="Token doğrulanamadı")
    
    @staticmethod
    def check_username(username: str) -> None:
        user = DBService.auth.find_one({"username": username})
        print(user)
        if user is not None:
            raise Exception("kullanıcı adı zaten bulunuyor.")
    
    @staticmethod
    def check_email(email: str) -> None:
        user_mail = DBService.auth.find_one({"email": email})
        if user_mail is not None:
            raise Exception("zaten aynı email adresi bulunuyor")
    
    @staticmethod
    def login_user(username: str, password: str) -> bool:
        try:
            user_data = DBService.auth.find_one({"username": username})
            if not user_data:
                print("kullanıcı bulunamadı.")
                return False
            
            password_hash = AuthService.hash_password(password)
            if password_hash != user_data["hashed_password"]:
                print("yanlış şifre")
                return False
            
            print("Giriş başarılı.")
            return   True
        except Exception as e:
            print(f"hata: {e}")
            return False

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    


    @staticmethod
    def get_user_by_id(user_id: int) -> dict:
        user = DBService.auth.find_one({"user_id": user_id}, {"_id": 0, "hashed_password": 0})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def update_user_email(user_id: int, update_data: UserUpdate) -> dict:
        updated_user = DBService.auth.find_one_and_update(
            {"user_id": user_id},
           {"$set": {"email": update_data.email}},
            return_document=ReturnDocument.AFTER,
            projection={"_id": 0, "hashed_password": 0}
        )
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found or update failed")
        return updated_user

    @staticmethod
    def delete_user(user_id: int) -> bool:
        result = DBService.auth.delete_one({"user_id": user_id})
        return result.deleted_count == 1



    @staticmethod
    def create_user_token(username: str, user_id):
        payload = {
            "sub": str(user_id),
            "username": username,
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "role":"user"
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
        return token

   
 
    @staticmethod
    def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
        try:
            payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            username = payload.get("username")
            role = payload.get("role")

            if user_id is None or username is None or role != "user":
                raise HTTPException(status_code=403, detail="Normal kullanıcı yetkisi gerekli")
            return {"user_id": int(user_id), "username": username, "role": role}
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token süresi dolmuş")
        except JWTError:
            raise HTTPException(status_code=401, detail="Token doğrulanamadı")




    @staticmethod
    def get_all_users() -> list:
        users = list(DBService.auth.find({}, {"_id": 0, "hashed_password": 0}))
        return users