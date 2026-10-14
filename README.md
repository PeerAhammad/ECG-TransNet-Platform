# ECG-TransNet Platform 🫀
### Explainable AI for ECG-Based Arrhythmia Classification

A full-stack healthcare AI research prototype that combines a PyTorch CNN–Transformer model with a React frontend and FastAPI backend to support ECG analysis, arrhythmia classification, prediction visualization, and explainability.

**Submission Type:** Individual  
**Contributor:** Peer Ahammad M. Bagawan  
**Institution:** Visvesvaraya Technological University (VTU), Belagavi, Karnataka, India  
**Domain:** Healthcare AI/ML  
**Project Status:** Research prototype

![Project Status](https://img.shields.io/badge/Status-Research%20Prototype-blue)
![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB)
![Backend](https://img.shields.io/badge/Backend-FastAPI-009688)
![Model](https://img.shields.io/badge/Model-PyTorch-EE4C2C)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 1. Overview

ECG-TransNet Platform is the application and deployment component of the ECG-TransNet arrhythmia-classification project. It connects a deep-learning model to a web interface so users can submit ECG data, inspect model predictions, and explore visual explanations of the output.

The platform integrates:

- A React and Vite frontend
- A FastAPI backend
- A PyTorch CNN–Transformer model
- ECG preprocessing and inference services
- Grad-CAM-based explainability functionality
- User authentication and analysis history

The goal is to explore how deep learning and explainable AI can support ECG signal analysis through an accessible software interface.

## 2. Problem Statement

Electrocardiograms (ECGs) are important tools for examining cardiac electrical activity. Automated ECG classification can help researchers investigate patterns associated with different heartbeat categories, but model outputs can be difficult to interpret when presented without supporting information.

ECG-TransNet addresses this software and research challenge by combining ECG classification with a web-based interface for viewing predictions, confidence information, processing time, and visual explanations.

The project is intended for research and educational evaluation. It is not a clinically validated diagnostic system.

## 3. Proposed Solution

The platform connects ECG input processing, deep-learning inference, and result visualization into one workflow.

1. **ECG input:** Submit ECG data through the application.
2. **Preprocessing:** Prepare the input for the trained model.
3. **Model inference:** Generate a classification using ECG-TransNet.
4. **Result visualization:** Present the predicted class and available prediction information.
5. **Explainability:** Display Grad-CAM-based visual analysis where supported.
6. **History:** Allow authenticated users to retrieve previous analysis results.

## 4. Key Features

### ECG Analysis
- ECG data upload and preprocessing
- Arrhythmia classification using the integrated model
- Prediction confidence display
- Processing-time information
- Analysis result visualization

### Explainable AI
- Grad-CAM-based model explanation functionality
- Visual exploration of ECG regions relevant to model predictions
- Dedicated explainability dashboard

Visual explanations indicate model behavior; they do not independently establish clinical significance.

### User and History Management
- User registration and authentication
- Analysis history
- Retrieval of previous predictions
- Results visualization

### Web Application
- React-based user interface
- FastAPI inference backend
- Separate frontend and backend components
- API documentation through FastAPI's interactive documentation interface

## 5. Technology Stack

| Component | Technology |
|---|---|
| Frontend | React, Vite, JavaScript |
| Backend | Python, FastAPI |
| Deep learning | PyTorch |
| Model architecture | 1D CNN–Transformer |
| Explainability | Grad-CAM |
| API communication | HTTP-based API endpoints |
| Version control | Git, GitHub |

## 6. AI/ML Model

The platform integrates the ECG-TransNet model developed for ECG arrhythmia classification.

The model combines:

- **1D convolutional layers:** Extract local patterns from ECG signals.
- **Transformer-based components:** Model temporal relationships in the input representation.
- **Preprocessing:** Prepare ECG data for inference.
- **Explainability:** Provide Grad-CAM-based visual analysis where supported by the implementation.

The backend model artifact is located at:

`ecg-transnet-api/ml_model/ecg_transnet.pt`

For the model implementation, training and evaluation details, visit the [ECG-TransNet Arrhythmia Detection repository](https://github.com/PeerAhammad/ECG-TransNet-Arrhythmia-Detection).

## 7. Reported Evaluation Results

The following results have been reported for the project. They should be interpreted alongside the corresponding evaluation scripts, dataset split, hardware configuration, and measurement methodology.

| Metric | Reported Result |
|---|---:|
| Overall accuracy | Approximately 98.2% |
| Average F1-score | Approximately 0.94 |
| Inference latency | Below 12 ms |
| Quantized model size | Approximately 27.4 MB |

**Evaluation notes**

- The precise dataset, test-set construction, and evaluation procedure should be documented alongside the accuracy and F1-score.
- Specify whether the F1-score is macro-averaged, weighted, or calculated using another method.
- Document the hardware, batch size, and timing procedure used for the latency measurement.
- Clarify the quantization method and exact artifact measured for model size.
- Do not interpret these model results as evidence of clinical effectiveness or diagnostic reliability.

The reported metrics describe model-level evaluation and may not represent end-to-end response time for the full web application.

## 8. System Architecture

At a high level, the application follows this workflow:

```text
                   ECG-TransNet Platform
                            |
              +-------------+-------------+
              |                           |
              v                           v
        React Frontend              FastAPI Backend
              |                           |
              |                  +--------+--------+
              |                  |                 |
              |                  v                 v
              |             Preprocessing      Inference
              |                                    |
              |                                    v
              |                            PyTorch Model
              |                                    |
              |                      +-------------+------------+
              |                      |                          |
              v                      v                          v
        Results and History     Predictions                Grad-CAM
                                and Confidence             Explanations
```

A separate architecture diagram will be provided as a submission document.

## 9. Repository Structure

```text
ECG-TransNet-Platform/
├── ecg-transnet-api/
│   ├── app/
│   │   ├── database/
│   │   │   └── db.py
│   │   ├── models/
│   │   │   └── schemas.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── history.py
│   │   │   ├── predict.py
│   │   │   └── xai.py
│   │   ├── services/
│   │   │   ├── ecg_transnet_model.py
│   │   │   ├── gradcam.py
│   │   │   ├── inference.py
│   │   │   └── preprocessing.py
│   │   ├── utils/
│   │   │   ├── auth_utils.py
│   │   │   └── report.py
│   │   └── main.py
│   ├── ml_model/
│   │   └── ecg_transnet.pt
│   ├── tests/
│   │   └── test_predict.py
│   └── requirements.txt
├── ecg-transnet-frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── sample_ecg_test.csv
├── .gitignore
└── README.md
```

This tree summarizes the current documented structure. Refer to the repository for the complete and up-to-date file listing.

## 10. Getting Started

### Prerequisites

- Python compatible with the backend dependencies
- pip
- Node.js and npm
- Git

### Clone the repository

```bash
git clone https://github.com/PeerAhammad/ECG-TransNet-Platform.git
cd ECG-TransNet-Platform
```

### Start the backend

```bash
cd ecg-transnet-api
python -m venv .venv
```

Activate the environment.

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Configure any required environment variables according to the project's configuration files. Do not commit secrets or production credentials.

Start the API:

```bash
uvicorn app.main:app --reload
```

The API is typically available at `http://127.0.0.1:8000`.

Interactive API documentation is typically available at `http://127.0.0.1:8000/docs`.

### Start the frontend

Open a separate terminal from the repository root:

```bash
cd ecg-transnet-frontend
npm install
npm run dev
```

Vite will display the local development URL, typically `http://localhost:5173`.

**Note:** Successful execution depends on the required model artifact, environment configuration, dependencies, and backend/frontend connection settings being present.

## 11. Testing

The backend includes prediction-related tests.

From the backend directory, install the dependencies and run:

```bash
pytest
```

Test coverage and results should be interpreted according to the tests actually included in the repository.

## 12. Example Output

The following is an illustrative example of the type of result the application may display. It is not a benchmark record or clinical assessment.

```text
Predicted Class:   N
Confidence:        97.1%
Risk Category:     Low
Processing Time:   0.209 s
Beats Analysed:    14
Model Version:     ECG-TransNet-v1.0
Predicted Rhythm:  Normal Beat
```

The output fields and values depend on the model, input data, and application implementation. Do not interpret an example confidence score as a probability of being clinically healthy.

## 13. Demo and Project Materials

- **Live application:** Add the public deployment URL when available.
- **Demo video:** Add the unlisted YouTube walkthrough URL when ready.
- **Architecture diagram:** Add the architecture PDF or image when ready.
- **Project presentation:** Add the presentation PDF when ready.

These resources will be added after they have been created and verified.

## 14. Research Context and Related Repositories

ECG-TransNet Platform is the full-stack application component of the broader ECG-TransNet project.

- [ECG-TransNet Platform — Main application repository](https://github.com/PeerAhammad/ECG-TransNet-Platform)
- [ECG-TransNet Arrhythmia Detection — Model and research repository](https://github.com/PeerAhammad/ECG-TransNet-Arrhythmia-Detection)
- [GitHub Profile](https://github.com/PeerAhammad)
- [ORCID](https://orcid.org/0009-0008-6686-9223)

The model repository should be consulted for the exact training configuration, datasets, evaluation scripts, and research methodology.

## 15. Limitations and Medical Disclaimer

ECG-TransNet Platform is a research and software-development prototype. It is not a certified medical device and has not been established by this README as clinically validated.

- Model performance depends on the input data, preprocessing, model version, and evaluation conditions.
- Confidence scores and visual explanations may not reflect clinical certainty.
- Grad-CAM visualizations do not prove causality or establish a diagnosis.
- Performance on research datasets does not guarantee generalization to different populations, devices, or clinical settings.
- Independent validation, appropriate clinical review, and applicable regulatory assessment are necessary before considering real-world medical use.

**Do not use this prototype to make medical decisions or replace assessment by a qualified healthcare professional.**

## 16. Project Status

**Status: Research prototype; deployment and submission materials are being finalized.**

The repository documents the frontend, backend, model integration, prediction workflow, authentication/history features, and explainability components. The availability of individual features depends on the current code and configuration.

## 17. License

This project is licensed under the [MIT License](LICENSE).

The license applies subject to its terms and does not automatically grant rights to third-party datasets, pretrained assets, or dependencies that may have separate licenses.
