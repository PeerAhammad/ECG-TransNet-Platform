"""
ECG-TransNet Inference Service
--------------------------------
Loads the trained model weights and runs beat-level arrhythmia classification.

Usage (called by FastAPI router):
    from app.services.inference import run_inference
    result = run_inference(beats)   # beats = output of preprocess_ecg()
"""

import os
import numpy as np
import torch
import torch.nn.functional as F

from app.services.ecg_transnet_model import ECGTransNet

# ── Constants ─────────────────────────────────────────────────────────────────
CLASSES    = ["N", "S", "V", "F", "Q"]
CLASS_NAMES = {
    "N": "Normal Beat",
    "S": "Supraventricular Ectopic",
    "V": "Ventricular Ectopic",
    "F": "Fusion Beat",
    "Q": "Unknown / Paced Beat",
}
RISK_MAP = {
    "N": "Low",
    "S": "Medium",
    "V": "High",
    "F": "Medium",
    "Q": "Critical",
}
MODEL_PATH    = os.getenv("MODEL_PATH", "ml_model/ecg_transnet.pt")
MODEL_VERSION = "ECG-TransNet-v1.0"

# ── Model hyperparameters ─────────────────────────────────────────────────────
# Must match exactly what was used during training.
MODEL_KWARGS = dict(
    n_classes = 5,
    d_model   = 128,
    n_heads   = 4,
    n_layers = 4,
    dim_ff    = 256,
    dropout   = 0.1,
)


# ── Singleton model loader ────────────────────────────────────────────────────

_model  = None
_device = None

def _load_model() -> tuple:
    """
    Load model once and cache globally.
    Returns (model, device).
    """
    global _model, _device

    if _model is not None:
        return _model, _device

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = ECGTransNet(**MODEL_KWARGS)
    state_dict = torch.load(MODEL_PATH, map_location=device)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()

    _model  = model
    _device = device
    print(f"[ECGTransNet] Model loaded on {device} from {MODEL_PATH}")
    return _model, _device


# ── Beat-level prediction ─────────────────────────────────────────────────────

def _predict_beats(beats: list, model: torch.nn.Module, device: torch.device) -> np.ndarray:
    """
    Run model on a list of beat segments.

    Args:
        beats  : list of np.ndarray, each shape (1, 187)
        model  : loaded ECGTransNet
        device : torch device

    Returns:
        probs  : np.ndarray of shape (n_beats, 5) — softmax probabilities
    """
    # Stack into batch tensor: (N, 1, 187)
    batch = np.stack(beats, axis=0)                         # (N, 1, 187)
    tensor = torch.tensor(batch, dtype=torch.float32).to(device)

    with torch.no_grad():
        logits = model(tensor)                              # (N, 5)
        probs  = F.softmax(logits, dim=1).cpu().numpy()    # (N, 5)

    return probs


# ── Aggregation ───────────────────────────────────────────────────────────────

def _aggregate_predictions(probs: np.ndarray) -> dict:
    """
    Aggregate beat-level probabilities into a single ECG-level result.

    Strategy:
      - Mean probability across all beats per class
      - Predicted class = argmax of mean probabilities
      - Confidence = mean probability of winning class
      - Per-beat breakdown available for XAI / visualisation

    Args:
        probs : (N, 5) — softmax probabilities per beat

    Returns:
        result dict with class, confidence, risk, probabilities, per_beat
    """
    mean_probs = probs.mean(axis=0)                         # (5,)
    predicted_idx   = int(np.argmax(mean_probs))
    predicted_class = CLASSES[predicted_idx]
    confidence      = float(mean_probs[predicted_idx])

    # Per-beat class predictions (useful for ECG highlight visualisation)
    per_beat_classes = [CLASSES[int(np.argmax(p))] for p in probs]

    return {
        "class":              predicted_class,
        "class_name":         CLASS_NAMES[predicted_class],
        "confidence":         round(confidence, 4),
        "risk":               RISK_MAP[predicted_class],
        "probabilities":      {cls: round(float(p), 4) for cls, p in zip(CLASSES, mean_probs)},
        "n_beats_analysed":   len(probs),
        "per_beat_classes":   per_beat_classes,
        "model_version":      MODEL_VERSION,
    }


# ── Public API ────────────────────────────────────────────────────────────────

def run_inference(beats: list) -> dict:
    """
    Main inference entry point called by the FastAPI /predict router.

    Args:
        beats : list of np.ndarray (1, 187) — output of preprocess_ecg()

    Returns:
        result : dict with keys:
            class, class_name, confidence, risk,
            probabilities, n_beats_analysed,
            per_beat_classes, model_version
    """
    if not beats:
        raise ValueError("No beat segments to classify.")

    model, device = _load_model()
    probs  = _predict_beats(beats, model, device)
    result = _aggregate_predictions(probs)
    return result

