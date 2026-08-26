# ECG-TransNet Frontend

React + Tailwind + Vite frontend for the ECG-TransNet platform.

## Quickstart

```bash
npm install
npm run dev
```

Visit http://localhost:5173

## Environment

Copy `.env` and set `VITE_API_URL` to your FastAPI backend URL.

## Pages

| Route      | Page              |
|------------|-------------------|
| /          | Landing           |
| /upload    | ECG Upload        |
| /results   | Prediction Result |
| /history   | Past Analyses     |
| /xai       | XAI Dashboard     |
| /login     | Login             |
| /register  | Register          |
