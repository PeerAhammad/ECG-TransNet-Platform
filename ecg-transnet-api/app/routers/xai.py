from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.preprocessing import preprocess_ecg
from app.services.inference import _load_model
from app.services.gradcam import generate_gradcam


router = APIRouter()


@router.post("/xai/gradcam")
async def gradcam_ecg(file: UploadFile = File(...)):

    if not file.filename.endswith((".csv", ".txt")):
        raise HTTPException(
            status_code=400,
            detail="Only .csv or .txt files accepted."
        )

    raw_bytes = await file.read()

    # Preprocess ECG
    try:
        beats = preprocess_ecg(raw_bytes)
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Preprocessing failed: {str(e)}"
        )

    if not beats:
        raise HTTPException(
            status_code=422,
            detail="No ECG beats detected."
        )

    # Load existing trained model
    model, device = _load_model()

    # Use first detected beat for visualization
    result = generate_gradcam(
        beat=beats[0],
        model=model,
        device=device
    )

    return {
        "filename": file.filename,
        "beat_index": 0,
        "n_beats_detected": len(beats),
        **result
    }