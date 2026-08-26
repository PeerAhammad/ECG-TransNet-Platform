"""
Database connection — MongoDB via motor.
Motor import is lazy (inside functions) so a broken motor install
does not crash the server on startup.
Prediction and inference endpoints work without DB.
DB is only needed for auth and history endpoints.
"""

import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME   = os.getenv("DB_NAME", "ecg_transnet")

_client = None

async def init_db():
    global _client
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        _client = AsyncIOMotorClient(MONGO_URL)
        print(f"Connected to MongoDB: {DB_NAME}")
    except Exception as e:
        print(f"[WARNING] MongoDB not available: {e}")
        print("[WARNING] Auth and History endpoints will not work, but /predict is unaffected.")
        _client = None

async def get_db():
    if _client is None:
        return None
    return _client[DB_NAME]
