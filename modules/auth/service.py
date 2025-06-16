from modules.auth.models.userCreate import UserCreate
from modules.db.service import DBService


class AuthService:
    def create_user(username: str, email: str, password: str) -> bool:
        try:
            DBService.auth.insert_one(
                UserCreate(
                    username=username,
                    email=email,
                    password=password
                ).model_dump()
            )
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False