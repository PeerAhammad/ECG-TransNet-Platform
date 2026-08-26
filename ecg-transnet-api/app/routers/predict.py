from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.inference import run_inference
from app.services.preprocessing import preprocess_ecg
from app.database.db import get_db
import time
import uuid
from datetime import datetime, timezone

router = APIRouter()


@router.post("/predict")
async def predict_ecg(
    file: UploadFile = File(...),
    db=Depends(get_db)
):
    if not file.filename.endswith((".csv", ".txt")):
        raise HTTPException(
            status_code=400,
            detail="Only .csv or .txt files accepted."
        )

    raw_bytes = await file.read()
    start = time.time()

    try:
        beats = preprocess_ecg(raw_bytes)
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Preprocessing failed: {str(e)}"
        )

    try:
        result = run_inference(beats)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Inference failed: {str(e)}"
        )

    processing_time = round(time.time() - start, 3)
    prediction_id = str(uuid.uuid4())

    prediction = {
        "prediction_id": prediction_id,
        "filename": file.filename,
        "predicted_class": result["class"],
        "class_name": result["class_name"],
        "confidence": result["confidence"],
        "risk_category": result["risk"],
        "class_probabilities": result["probabilities"],
        "n_beats_analysed": result["n_beats_analysed"],
        "per_beat_classes": result["per_beat_classes"],
        "processing_time_seconds": processing_time,
        "model_version": result["model_version"],
        "created_at": datetime.now(timezone.utc),
    }

    if db is not None:
        try:
            await db.predictions.insert_one(prediction)
        except Exception as e:
            print(f"[WARNING] Could not save prediction to MongoDB: {e}")

    prediction.pop("_id", None)
    return prediction