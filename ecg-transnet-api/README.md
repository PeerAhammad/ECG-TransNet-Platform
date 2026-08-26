# ECG-TransNet API

FastAPI backend for the ECG-TransNet Arrhythmia Detection Platform.

## Quickstart

```bash
pip install -r requirements.txt
cp .env.example .env       # fill in your values
uvicorn app.main:app --reload
```

API docs auto-generated at: http://localhost:8000/docs

## Key Endpoints

| Method | Path               | Description              |
|--------|--------------------|--------------------------|
| POST   | /api/v1/predict    | Upload ECG, get result   |
| POST   | /api/v1/register   | Register user            |
| POST   | /api/v1/login      | Login, get JWT           |
| GET    | /api/v1/history    | Get prediction history   |

## Next Steps

1. Port your preprocessing pipeline into `app/services/preprocessing.py`
2. Load your trained model in `app/services/inference.py`
3. Connect MongoDB Atlas in `.env`
