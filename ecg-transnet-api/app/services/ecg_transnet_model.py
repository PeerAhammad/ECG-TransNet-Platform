"""
ECG-TransNet model architecture matching the supplied trained checkpoint.

Input:
    (batch, 1, 187)

Output:
    (batch, 5)

Classes:
    N, S, V, F, Q
"""

import torch
import torch.nn as nn


class ECGTransNet(nn.Module):
    """
    Architecture reconstructed to match ml_model/ecg_transnet.pt.

    Pipeline:

        Input (B, 1, 187)
            ↓
        Conv1D 1 → 128, kernel=7, stride=3, padding=3
            ↓
        BatchNorm1D
            ↓
        ReLU
            ↓
        (B, 128, 63)
            ↓
        Permute
            ↓
        (B, 63, 128)
            ↓
        Positional Embedding
            ↓
        4-layer Transformer Encoder
            ↓
        Global Average Pooling
            ↓
        Linear 128 → 5
    """

    def __init__(
        self,
        n_classes: int = 5,
        d_model: int = 128,
        n_heads: int = 4,
        n_layers: int = 4,
        dim_ff: int = 256,
        dropout: float = 0.1,
    ):
        super().__init__()

        # ---------------------------------------------------------
        # CNN feature extractor
        # ---------------------------------------------------------
        #
        # 187 input samples -> 63 temporal positions
        #
        self.cnn_features = nn.Sequential(
            nn.Conv1d(
                in_channels=1,
                out_channels=128,
                kernel_size=7,
                stride=3,
                padding=3,
                bias=True,
            ),
            nn.BatchNorm1d(128),
            nn.ReLU(inplace=True),
        )

        # ---------------------------------------------------------
        # Learnable positional embedding
        # ---------------------------------------------------------
        #
        # The checkpoint contains:
        # pos_embedding: (1, 63, 128)
        #
        self.pos_embedding = nn.Parameter(
            torch.zeros(1, 63, d_model)
        )

        # ---------------------------------------------------------
        # Transformer encoder
        # ---------------------------------------------------------

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=n_heads,
            dim_feedforward=dim_ff,
            dropout=dropout,
            activation="relu",
            batch_first=True,
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=n_layers,
        )

        # ---------------------------------------------------------
        # Classification head
        # ---------------------------------------------------------

        self.classifier = nn.Linear(
            d_model,
            n_classes,
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x:
                Tensor of shape (B, 1, 187)

        Returns:
            logits:
                Tensor of shape (B, 5)
        """

        # CNN
        x = self.cnn_features(x)

        # (B, 128, 63) -> (B, 63, 128)
        x = x.transpose(1, 2)

        # Add learned positional embedding
        x = x + self.pos_embedding[:, :x.size(1), :]

        # Transformer
        x = self.transformer(x)

        # Global average pooling
        x = x.mean(dim=1)

        # Classification
        logits = self.classifier(x)

        return logits