from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Dict, Optional

# ── Prediction ─────────────────────────────────────────────
class PredictionResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())  # allow "model_*" field names

    prediction_id: str
    predicted_class: str          # N, S, V, F, Q
    confidence: float             # 0.0 – 1.0
    risk_category: str            # Low / Medium / High / Critical
    processing_time_seconds: float
    model_version: str
    class_probabilities: Dict[str, float]

# ── Auth ───────────────────────────────────────────────────
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
