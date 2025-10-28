import os
from typing import Optional


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self) -> None:
        self.model_name: str = os.getenv("MODEL_NAME", "yolov8n.pt")
        self.device: Optional[str] = os.getenv("DEVICE", None)  # e.g., "cpu", "cuda"
        # Prediction defaults
        self.conf_threshold: float = float(os.getenv("CONF_THRESHOLD", "0.25"))
        self.iou_threshold: float = float(os.getenv("IOU_THRESHOLD", "0.45"))
        self.max_detections: int = int(os.getenv("MAX_DETECTIONS", "300"))


settings = Settings()
