# ECG-TransNet Platform

Full-stack deployment of the ECG-TransNet Arrhythmia Detection System.

## Structure

| Folder                   | Purpose                         |
|--------------------------|---------------------------------|
| ecg-transnet-api/        | FastAPI backend + ML inference  |
| ecg-transnet-frontend/   | React + Tailwind frontend       |

## Getting Started

### Backend
```bash
cd ecg-transnet-api
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### Frontend
```bash
cd ecg-transnet-frontend
npm install
npm run dev
```

## Deployment

- Backend  → Render (connect GitHub repo, set env vars)
- Frontend → Vercel (connect GitHub repo, set VITE_API_URL)
