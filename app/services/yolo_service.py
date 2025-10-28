from __future__ import annotations

from typing import Any, List

import numpy as np
from PIL import Image
from ultralytics import YOLO

from app.core.config import settings
from app.schemas import BBox, Detection


class YOLOService:
    def __init__(self) -> None:
        self.model_name = settings.model_name
        self.device = settings.device
        self.model = YOLO(self.model_name)
        if self.device:
            self.model.to(self.device)

    def predict_image(self, image: Image.Image) -> List[Detection]:
        # Run inference with configured thresholds
        results = self.model.predict(
            source=np.array(image),
            conf=settings.conf_threshold,
            iou=settings.iou_threshold,
            max_det=settings.max_detections,
            verbose=False,
        )
        detections: List[Detection] = []

        if not results:
            return detections

        r0 = results[0]
        names = r0.names  # class id -> name
        boxes = r0.boxes  # Boxes object
        if boxes is None or boxes.data is None:
            return detections

        # boxes.data: [x1, y1, x2, y2, conf, cls]
        data = boxes.data.cpu().numpy() if hasattr(boxes.data, "cpu") else boxes.data
        for x1, y1, x2, y2, conf, cls_id in data:
            cls_int = int(cls_id)
            det = Detection(
                class_id=cls_int,
                class_name=names.get(cls_int, str(cls_int)) if isinstance(names, dict) else str(cls_int),
                confidence=float(conf),
                bbox=BBox(x1=float(x1), y1=float(y1), x2=float(x2), y2=float(y2)),
            )
            detections.append(det)
        return detections


# Singleton accessor
_yolo_service: YOLOService | None = None


def get_yolo_service() -> YOLOService:
    global _yolo_service
    if _yolo_service is None:
        _yolo_service = YOLOService()
    return _yolo_service
