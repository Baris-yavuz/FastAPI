from fastapi import APIRouter, HTTPException, Depends
from modules.auth.service import AuthService
from modules.db.service import DBService 
from modules.auth.models.userUptade import UserUpdate



router = APIRouter()
routerAdmin = APIRouter()

    
@router.post("/user/register")
def register(username: str, email: str, password: str) -> bool:
     try:
        return AuthService.create_user(username=username, email=email, password=password
        )
     except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
     
  


@router.post("/user/login")
def login(username: str, password: str):
    success = AuthService.login_user(username, password)
    if not success:
        raise HTTPException(status_code=401, detail="Geçersiz kullanıcı adı veya şifre")
    
    # Veritabanından user_id'yi çekiyoruz
    user_data = DBService.auth.find_one({"username": username})
    if not user_data:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    user_id = user_data.get("user_id")

    token = AuthService.create_user_token(username=username, user_id = str(user_id))

    return {
        "message": "Giriş başarılı",
        "access_token": token,
        "token_type": "bearer"
    }



@router.get("/user/me")
def get_User(current_user: dict = Depends(AuthService.get_current_user)):
    return current_user


@routerAdmin.post("/register")
def register_admin(username: str, email: str, password: str):
    try:
        result = AuthService.create_admin(username=username, email=email, password=password)
        if result:
            return {"message": "Admin başarıyla oluşturuldu"}
        else:
            raise HTTPException(status_code=400, detail="Admin oluşturulamadı")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@routerAdmin.post("/login")
def admin_login(username: str, password: str):
    success = AuthService.login_admin(username, password)
    if not success:
        raise HTTPException(status_code=401, detail="Geçersiz admin kullanıcı adı veya şifre")
    
    admin_data = DBService.admin.find_one({"username": username})
    if not admin_data:
        raise HTTPException(status_code=404, detail="Admin bulunamadı")
    
    admin_id = admin_data.get("admin_id")
    token = AuthService.create_admin_token(username=username, admin_id=str(admin_id))

    return {
        "message": "Admin girişi başarılı",
        "access_token": token,
        "token_type": "bearer"
    }

@routerAdmin.get("/me")
def get_admin(current_admin: dict = Depends(AuthService.get_current_admin)):
    return current_admin

@routerAdmin.get("/users")
def list_all_users(current_admin: dict = Depends(AuthService.get_current_admin)):
    return {"users": AuthService.get_all_users()}

@routerAdmin.put("/user->uptadeMail")
def admin_update_user(user_id: int, email: str, current_admin: dict = Depends(AuthService.get_current_admin)):
    update = UserUpdate(email=email)
    return AuthService.update_user_email(user_id, update)

@routerAdmin.delete("/user->delete")
def admin_delete_user(user_id: int, current_admin: dict = Depends(AuthService.get_current_admin)):
    success = AuthService.delete_user(user_id)
    if success:
        return {"detail": f"User ID {user_id} admin tarafından silindi"}
    raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

