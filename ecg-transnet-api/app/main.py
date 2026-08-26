from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import predict, auth, history, xai
from app.database.db import init_db

app = FastAPI(
    title="ECG-TransNet API",
    description="Arrhythmia Detection Platform powered by Hybrid CNN-Transformer",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(
    predict.router,
    prefix="/api/v1",
    tags=["Prediction"]
)

app.include_router(
    auth.router,
    prefix="/api/v1",
    tags=["Auth"]
)

app.include_router(
    history.router,
    prefix="/api/v1",
    tags=["History"]
)

app.include_router(
    xai.router,
    prefix="/api/v1",
    tags=["XAI"]
)

@app.get("/")
def root():
    return {
        "message": "ECG-TransNet API is running",
        "version": "1.0.0"
    }
