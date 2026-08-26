# ECG-TransNet Platform 🫀

> A full-stack web platform for ECG arrhythmia analysis using the ECG-TransNet deep-learning model, with a React frontend, FastAPI backend, model inference, history tracking, and explainable AI.

![Status](https://img.shields.io/badge/Status-Research%20Prototype-blue)
![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB)
![Backend](https://img.shields.io/badge/Backend-FastAPI-009688)
![Model](https://img.shields.io/badge/Model-PyTorch-EE4C2C)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Overview

**ECG-TransNet Platform** is the web application layer built around the ECG-TransNet arrhythmia-classification model.

The platform provides a complete workflow for:

```text
ECG Data
   ↓
Upload / Input
   ↓
Preprocessing
   ↓
ECG-TransNet Inference
   ↓
Arrhythmia Prediction
   ↓
Confidence & Risk Information
   ↓
Explainable AI
   ↓
Results / History
```

The project combines a **React frontend** with a **FastAPI backend** and a PyTorch ECG-TransNet model.

---

## ✨ Features

### ECG Analysis

* Upload ECG data for analysis
* ECG preprocessing before inference
* Arrhythmia classification using ECG-TransNet
* Prediction confidence display
* Processing-time information
* Analysis summary

### Explainable AI

The platform includes explainability functionality for investigating model predictions.

Current backend components include:

```text
ecg-transnet-api/app/services/
├── inference.py
├── preprocessing.py
└── gradcam.py
```

The frontend provides an XAI dashboard for presenting model explanations.

### User & History Features

The platform includes:

* User registration
* User authentication
* Analysis history
* Previous prediction retrieval
* Results visualization

### Frontend

The React frontend includes dedicated pages for:

* Landing
* Login
* Registration
* ECG upload
* Results
* History
* XAI dashboard

---

## 🏗️ System Architecture

```text
                   ECG-TransNet Platform
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
      React / Vite Frontend       FastAPI Backend
              │                         │
              │                   ┌─────┴─────┐
              │                   │           │
              │                   ▼           ▼
              │              Preprocessing  Inference
              │                               │
              │                               ▼
              │                       ECG-TransNet
              │                         PyTorch Model
              │                               │
              │                    ┌──────────┴──────────┐
              │                    │                     │
              ▼                    ▼                     ▼
          Results             Prediction             Grad-CAM
          History             Confidence            Explainability
```

---

## 📁 Project Structure

```text
ECG-TransNet-Platform/
│
├── ecg-transnet-api/
│   ├── app/
│   │   ├── database/
│   │   │   └── db.py
│   │   │
│   │   ├── models/
│   │   │   └── schemas.py
│   │   │
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── history.py
│   │   │   ├── predict.py
│   │   │   └── xai.py
│   │   │
│   │   ├── services/
│   │   │   ├── ecg_transnet_model.py
│   │   │   ├── gradcam.py
│   │   │   ├── inference.py
│   │   │   └── preprocessing.py
│   │   │
│   │   ├── utils/
│   │   │   ├── auth_utils.py
│   │   │   └── report.py
│   │   │
│   │   └── main.py
│   │
│   ├── ml_model/
│   │   └── ecg_transnet.pt
│   │
│   ├── tests/
│   │   └── test_predict.py
│   │
│   └── requirements.txt
│
├── ecg-transnet-frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ui/
│   │   │       └── Navbar.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── HistoryPage.jsx
│   │   │   ├── LandingPage.jsx
│   │   │   ├── LoginPage.jsx
│   │   │   ├── RegisterPage.jsx
│   │   │   ├── ResultsPage.jsx
│   │   │   ├── UploadPage.jsx
│   │   │   └── XAIDashboard.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── sample_ecg_test.csv
├── .gitignore
└── README.md
```

---

## 🧠 Model

The platform uses the **ECG-TransNet** model developed for ECG arrhythmia classification.

The model combines:

* 1D convolutional feature extraction
* Transformer-based temporal modeling
* ECG preprocessing
* Explainable AI analysis

The trained model used by the API is:

```text
ecg-transnet-api/ml_model/ecg_transnet.pt
```

For details about the underlying research model, see:

🔗 [ECG-TransNet Research Repository](https://github.com/PeerAhammad/ECG-TransNet-Arrhythmia-Detection)

---

## ⚙️ Backend Setup

### Requirements

* Python 3.8+
* pip
* PyTorch
* FastAPI

Install backend dependencies:

```bash
cd ecg-transnet-api
pip install -r requirements.txt
```

### Environment Variables

Create a local `.env` file based on:

```text
.env.example
```

Do not commit secrets or production environment variables.

### Start the API

From the backend directory:

```bash
uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🌐 Frontend Setup

Install the frontend dependencies:

```bash
cd ecg-transnet-frontend
npm install
```

Start the development server:

```bash
npm run dev
```

The Vite development server will provide a local URL, typically:

```text
http://localhost:5173
```

---

## 🔄 Application Workflow

### 1. Upload

The user provides ECG data through the upload interface.

### 2. Preprocessing

The backend prepares the input for the ECG-TransNet model.

### 3. Inference

The trained PyTorch model generates an arrhythmia prediction.

### 4. Results

The frontend displays:

* Predicted class
* Confidence
* Risk category
* Processing time
* Analysis summary

### 5. Explainability

Grad-CAM-based analysis can be used to inspect regions of the ECG signal contributing to the model output.

### 6. History

Authenticated users can access previous analysis results.

---

## 🧪 Testing

The backend includes prediction-related tests:

```bash
cd ecg-transnet-api
pytest
```

---

## 📊 Example Result

A typical analysis result presented by the platform includes:

```text
Predicted Class:   N
Confidence:        97.1%
Risk Category:     Low
Processing Time:   0.209 s
Beats Analysed:    14
Model Version:     ECG-TransNet-v1.0
Predicted Rhythm:  Normal Beat
```

These values are example application output and are not intended as clinical validation.

---

## 🛡️ Important Disclaimer

This project is a **research and software-development prototype**.

The predictions generated by the system should **not be treated as a medical diagnosis or a substitute for evaluation by a qualified healthcare professional**.

Model performance, confidence scores, and risk labels depend on the input data and the trained model and require appropriate clinical validation before any real-world medical use.

---

## 🚀 Deployment

The project is structured for separate deployment of:

```text
React Frontend
       +
FastAPI Backend
       +
PyTorch Model
```

The GitHub repository contains the source code and model required for the current prototype.

A public live-demo URL can be added here once deployment is completed:

```text
🌐 Live Demo: Coming soon
```

---

## 🔬 Research Context

ECG-TransNet Platform is the deployment/application component of the broader ECG-TransNet research project.

The research work focuses on:

* ECG arrhythmia classification
* CNN–Transformer architectures
* Multi-dataset evaluation
* Class imbalance
* Explainable AI

### Related Links

* [ECG-TransNet Research Repository](https://github.com/PeerAhammad/ECG-TransNet-Arrhythmia-Detection)
* [ORCID](https://orcid.org/0009-0008-6686-9223)
* [OpenReview](https://openreview.net/profile?id=%7EPeerAhammad_M_Bagawan3)
* [GitHub Profile](https://github.com/PeerAhammad)

---

## 📌 Project Status

**Research prototype — full-stack implementation completed and deployment in progress.**

The current repository contains the frontend, backend, trained model, authentication/history functionality, inference pipeline, and explainability components.

---

## License

See the repository license file for licensing information.
