from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import UserCreate, UserLogin, TokenResponse
from app.database.db import get_db
from app.utils.auth_utils import hash_password, create_jwt

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
async def register(user: UserCreate, db=Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable.")
    hashed = hash_password(user.password)
    token  = create_jwt({"sub": user.email})
    return TokenResponse(access_token=token, token_type="bearer")

@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, db=Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable.")
    token = create_jwt({"sub": user.email})
    return TokenResponse(access_token=token, token_type="bearer")
