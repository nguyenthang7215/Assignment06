from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


class ImageService:
    """Converts an image into a compact color-and-layout feature vector."""

    GRID_SIZE = 3

    def __init__(self, mode: str = "color") -> None:
        if mode not in {"color", "mobilenet"}:
            raise ValueError(f"Unknown image encoder: {mode}")
        self.mode = mode
        if mode == "mobilenet":
            import torch
            from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small

            weights = MobileNet_V3_Small_Weights.DEFAULT
            model = mobilenet_v3_small(weights=weights).eval()
            self._model = torch.nn.Sequential(model.features, model.avgpool, torch.nn.Flatten())
            self._preprocess = weights.transforms()

    def encode(self, image_path: Path) -> np.ndarray:
        image_path = Path(image_path)
        if not image_path.is_file():
            raise FileNotFoundError(f"Image not found: {image_path}")
        if self.mode == "mobilenet":
            import torch

            with Image.open(image_path) as source:
                tensor = self._preprocess(source.convert("RGB")).unsqueeze(0)
            with torch.no_grad():
                vector = self._model(tensor).squeeze(0).numpy()
            norm = float(np.linalg.norm(vector))
            return vector / norm if norm else vector
        with Image.open(image_path) as source:
            image = source.convert("RGB").resize((96, 96))
            pixels = np.asarray(image, dtype=np.float32) / 255.0

        # Global color distribution: 8 bins per channel.
        histogram_parts = [
            np.histogram(pixels[:, :, channel], bins=8, range=(0.0, 1.0))[0]
            for channel in range(3)
        ]
        histogram = np.concatenate(histogram_parts).astype(np.float32)
        histogram /= max(float(histogram.sum()), 1.0)

        # A 3x3 spatial color grid preserves rough shape and color placement.
        blocks: list[np.ndarray] = []
        step = 96 // self.GRID_SIZE
        for row in range(self.GRID_SIZE):
            for column in range(self.GRID_SIZE):
                block = pixels[
                    row * step : (row + 1) * step,
                    column * step : (column + 1) * step,
                ]
                blocks.append(block.mean(axis=(0, 1)))
        vector = np.concatenate((histogram, np.concatenate(blocks)))
        norm = float(np.linalg.norm(vector))
        return vector / norm if norm else vector
