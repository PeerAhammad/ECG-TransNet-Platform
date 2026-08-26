"""
ECG-TransNet Preprocessing Pipeline
-------------------------------------
Converts raw ECG CSV/TXT bytes → list of normalised beat tensors (187 samples each).

Pipeline steps (matching MIT-BIH / AAMI EC57 standard):
  1. Parse raw signal from CSV or TXT
  2. Butterworth Bandpass Filter   (0.5 – 35 Hz, 360 Hz sample rate)
  3. Baseline Wander Removal       (median filter subtraction)
  4. Z-Score Normalisation
  5. R-Peak Detection              (Pan-Tompkins inspired: diff + square + moving window)
  6. Beat Segmentation             (window centred on each R-peak → 187 samples)

Output: list of np.ndarray, each shape (1, 187) — ready for model input
"""

import io
import numpy as np
from scipy.signal import butter, filtfilt, medfilt

# ── Constants ─────────────────────────────────────────────────────────────────
FS            = 360          # MIT-BIH sampling rate (Hz)
BEAT_LEN      = 187          # fixed beat segment length (samples)
PRE_R         = 90           # samples before R-peak
POST_R        = BEAT_LEN - PRE_R   # samples after R-peak (97)
LOWCUT        = 0.5          # bandpass lower bound (Hz)
HIGHCUT       = 35.0         # bandpass upper bound (Hz)
FILTER_ORDER  = 4            # Butterworth filter order


# ── Step 1: Parse raw bytes → numpy signal ────────────────────────────────────

def parse_signal(raw_bytes: bytes) -> np.ndarray:
    """
    Accept CSV or whitespace-delimited TXT.
    Reads the first numeric column; skips header lines automatically.
    """
    text = raw_bytes.decode("utf-8", errors="ignore")
    values = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Take first comma- or whitespace-separated token
        token = line.split(",")[0].split()[0] if line.split(",")[0].split() else ""
        try:
            values.append(float(token))
        except ValueError:
            continue  # skip header / non-numeric rows

    if len(values) < BEAT_LEN:
        raise ValueError(
            f"Signal too short: got {len(values)} samples, need at least {BEAT_LEN}."
        )
    return np.array(values, dtype=np.float32)


# ── Step 2: Butterworth Bandpass Filter ───────────────────────────────────────

def bandpass_filter(signal: np.ndarray) -> np.ndarray:
    """Remove low-frequency drift and high-frequency noise."""
    nyq = FS / 2.0
    low  = LOWCUT  / nyq
    high = HIGHCUT / nyq
    b, a = butter(FILTER_ORDER, [low, high], btype="band")
    return filtfilt(b, a, signal).astype(np.float32)


# ── Step 3: Baseline Wander Removal ──────────────────────────────────────────

def remove_baseline_wander(signal: np.ndarray) -> np.ndarray:
    """
    Two-pass median filter subtraction.
      Pass 1: kernel = 200 ms  (≈ P/T wave width)
      Pass 2: kernel = 600 ms  (≈ one full cycle)
    Ensures kernel sizes are odd integers.
    """
    def odd(n):
        n = int(n)
        return n if n % 2 == 1 else n + 1

    k1 = odd(0.2 * FS)   # ~72 samples
    k2 = odd(0.6 * FS)   # ~216 samples
    baseline = medfilt(medfilt(signal, k1), k2)
    return (signal - baseline).astype(np.float32)


# ── Step 4: Z-Score Normalisation ────────────────────────────────────────────

def z_score_normalise(signal: np.ndarray) -> np.ndarray:
    mean = signal.mean()
    std  = signal.std()
    if std < 1e-8:
        std = 1e-8   # guard against flat signal
    return ((signal - mean) / std).astype(np.float32)


# ── Step 5: R-Peak Detection (Pan-Tompkins inspired) ─────────────────────────

def detect_r_peaks(signal: np.ndarray) -> np.ndarray:
    """
    Lightweight Pan-Tompkins inspired detector:
      differentiate → square → moving-window integration → threshold → peak localisation.
    Returns array of R-peak sample indices.
    """
    # Derivative
    diff = np.diff(signal, prepend=signal[0])

    # Squaring (emphasise large slopes)
    squared = diff ** 2

    # Moving-window integration (~150 ms window)
    win = int(0.15 * FS)
    kernel = np.ones(win) / win
    integrated = np.convolve(squared, kernel, mode="same")

    # Adaptive threshold: 50% of mean of top 10%
    threshold = np.percentile(integrated, 90) * 0.5

    # Find candidate peaks above threshold
    above = (integrated > threshold).astype(np.int8)
    edges = np.diff(above, prepend=0)
    starts = np.where(edges == 1)[0]
    ends   = np.where(edges == -1)[0]

    # Pad ends if signal ends while above threshold
    if len(ends) < len(starts):
        ends = np.append(ends, len(signal) - 1)

    r_peaks = []
    min_rr = int(0.2 * FS)   # minimum 200 ms between beats

    for s, e in zip(starts, ends):
        segment = signal[s:e]
        if len(segment) == 0:
            continue
        local_max = s + np.argmax(np.abs(segment))
        # Enforce minimum RR interval
        if r_peaks and (local_max - r_peaks[-1]) < min_rr:
            continue
        r_peaks.append(local_max)

    return np.array(r_peaks, dtype=np.int32)


# ── Step 6: Beat Segmentation ─────────────────────────────────────────────────

def segment_beats(signal: np.ndarray, r_peaks: np.ndarray) -> list:
    """
    Extract a fixed-length window of BEAT_LEN (187) samples centred on each R-peak.
    Windows that extend outside the signal boundaries are zero-padded.
    Returns list of np.ndarray, each shape (1, 187).
    """
    beats = []
    sig_len = len(signal)

    for r in r_peaks:
        start = r - PRE_R
        end   = r + POST_R

        if start < 0 or end > sig_len:
            # Zero-pad boundary beats
            beat = np.zeros(BEAT_LEN, dtype=np.float32)
            sig_start = max(0, start)
            sig_end   = min(sig_len, end)
            beat_start = sig_start - start
            beat_end   = beat_start + (sig_end - sig_start)
            beat[beat_start:beat_end] = signal[sig_start:sig_end]
        else:
            beat = signal[start:end].copy()

        # Per-beat normalisation (keeps each beat on the same scale)
        beat = (beat - beat.mean()) / (beat.std() + 1e-8)
        beats.append(beat.reshape(1, BEAT_LEN))   # shape: (1, 187)

    return beats


# ── Public API ────────────────────────────────────────────────────────────────

def preprocess_ecg(raw_bytes: bytes) -> list:
    """
    Full preprocessing pipeline.

    Args:
        raw_bytes : raw content of uploaded .csv or .txt file

    Returns:
        beats : list of np.ndarray, each (1, 187) — normalised beat segments
                ready to be stacked into a batch tensor for ECGTransNet

    Raises:
        ValueError : if the file is unparseable or the signal is too short
    """
    signal = parse_signal(raw_bytes)
    signal = bandpass_filter(signal)
    signal = remove_baseline_wander(signal)
    signal = z_score_normalise(signal)
    r_peaks = detect_r_peaks(signal)

    if len(r_peaks) == 0:
        raise ValueError("No R-peaks detected. Check signal quality or file format.")

    beats = segment_beats(signal, r_peaks)
    return beats
