from fastapi import FastAPI
from app.api.routes.users import router as users_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Clean Architecture API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://tgbot-webappfront-7yjyaf0cf-lifanna1.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)

app.include_router(
    users_router,
    prefix="/api/v1/users",
    tags=["Users"]
)

@app.get("/")
async def root():
    return {"message": "API is running"}
