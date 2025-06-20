from fastapi import FastAPI
import uvicorn
from modules.auth.controller import router as auth_router
# from modules.controller.controller import router as kullanicilar_router
# from modules.admin import admin_controller


app = FastAPI() # burada web üzerinde api uygulaması başlattık.


# app.include_router(kullanicilar_router, prefix="/kullanicilar", tags=["kullanicilar"])
# app.include_router(admin_controller.router)

app.include_router(auth_router, prefix="/auth", tags=["auth"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)