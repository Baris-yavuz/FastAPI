from fastapi import FastAPI
import uvicorn
from modules.auth.controller import router as auth_router
from modules.auth.controller import routerAdmin as adminRouter


app = FastAPI(
    title="My API",
    docs_url="/docs",  # ← Bu satırı ekle
    redoc_url="/redoc"
    ) # burada web üzerinde api uygulaması başlattık.



app.include_router(auth_router, prefix="/auth", tags=["auth"])

app.include_router(adminRouter, prefix="/admin", tags=["admin"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)