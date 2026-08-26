from fastapi import APIRouter, Depends, HTTPException
from app.database.db import get_db

router = APIRouter()


@router.get("/history")
async def get_history(db=Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable.")

    cursor = db.predictions.find(
        {},
        {"_id": 0}
    ).sort("created_at", -1)

    history = await cursor.to_list(length=100)

    # Convert datetime to JSON-safe string
    for item in history:
        if "created_at" in item:
            item["created_at"] = item["created_at"].isoformat()

    return {"history": history}


@router.get("/history/{prediction_id}")
async def get_single(prediction_id: str, db=Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable.")

    prediction = await db.predictions.find_one(
        {"prediction_id": prediction_id},
        {"_id": 0}
    )

    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found.")

    if "created_at" in prediction:
        prediction["created_at"] = prediction["created_at"].isoformat()

    return prediction