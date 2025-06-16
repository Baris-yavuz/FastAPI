from fastapi import FastAPI
from kullanicilar.controller.controller import router as kullanicilar_router
from kullanicilar.admin import admin_controller


app = FastAPI() # burada web üzerinde api uygulaması başlattık.


app.include_router(kullanicilar_router, prefix="/kullanicilar", tags=["kullanicilar"])
app.include_router(admin_controller.router)

