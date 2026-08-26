import numpy as np
import torch

from app.services.ecg_transnet_model import ECGTransNet
from app.services.inference import MODEL_KWARGS, MODEL_PATH


CLASSES = ["N", "S", "V", "F", "Q"]


def generate_gradcam(
    beat: np.ndarray,
    model: ECGTransNet,
    device: torch.device,
    target_class: int | None = None,
):
    """
    Grad-CAM for ECGTransNet.

    Input:
        beat: numpy array with shape (1, 187)

    Returns:
        waveform: original ECG beat
        heatmap: Grad-CAM importance for each ECG sample
        target_class: predicted/target class
        class_name: class label
    """

    # (1, 1, 187)
    x = torch.tensor(
        beat,
        dtype=torch.float32,
        device=device
    ).unsqueeze(0)

    model.eval()
    model.zero_grad()

    activations = None
    gradients = None

    # ---------------------------------------------------------
    # Forward hook
    # ---------------------------------------------------------
    def forward_hook(module, input, output):
        nonlocal activations
        activations = output

    # ---------------------------------------------------------
    # Backward hook
    # ---------------------------------------------------------
    def backward_hook(module, grad_input, grad_output):
        nonlocal gradients
        gradients = grad_output[0]

    target_layer = model.cnn.layer3

    forward_handle = target_layer.register_forward_hook(forward_hook)
    backward_handle = target_layer.register_full_backward_hook(backward_hook)

    try:
        # Forward pass
        logits = model(x)

        probabilities = torch.softmax(logits, dim=1)

        # Use predicted class if target wasn't supplied
        if target_class is None:
            target_class = int(torch.argmax(logits, dim=1).item())

        # Backpropagate target class score
        score = logits[0, target_class]
        score.backward()

        # -----------------------------------------------------
        # Grad-CAM calculation
        # -----------------------------------------------------

        # activations:
        # (1, 128, 47)
        #
        # gradients:
        # (1, 128, 47)

        weights = gradients.mean(dim=2, keepdim=True)

        cam = (weights * activations).sum(dim=1)

        # ReLU
        cam = torch.relu(cam)

        # Remove batch dimension
        cam = cam.squeeze(0)

        # Normalize 0 → 1
        cam_min = cam.min()
        cam_max = cam.max()

        if (cam_max - cam_min) > 1e-8:
            cam = (cam - cam_min) / (cam_max - cam_min)
        else:
            cam = torch.zeros_like(cam)

        cam = cam.detach().cpu().numpy()

        # -----------------------------------------------------
        # Resize CAM from 47 → 187 ECG samples
        # -----------------------------------------------------

        cam_tensor = torch.tensor(
            cam,
            dtype=torch.float32
        ).view(1, 1, -1)

        heatmap = torch.nn.functional.interpolate(
            cam_tensor,
            size=187,
            mode="linear",
            align_corners=True
        )

        heatmap = heatmap.squeeze().numpy()

        waveform = beat.squeeze().astype(float).tolist()

        return {
            "waveform": waveform,
            "heatmap": heatmap.tolist(),
            "target_class": CLASSES[target_class],
            "target_class_index": target_class,
            "probabilities": probabilities[0].detach().cpu().numpy().tolist(),
        }

    finally:
        forward_handle.remove()
        backward_handle.remove()