from typing import List, Optional
from pydantic import BaseModel, Field


class BBox(BaseModel):
    x1: float = Field(..., description="Left coordinate of the bounding box")
    y1: float = Field(..., description="Top coordinate of the bounding box")
    x2: float = Field(..., description="Right coordinate of the bounding box")
    y2: float = Field(..., description="Bottom coordinate of the bounding box")


class Detection(BaseModel):
    class_id: int
    class_name: str
    confidence: float
    bbox: BBox


class PredictResponse(BaseModel):
    model: str
    num_detections: int
    detections: List[Detection]


class HealthResponse(BaseModel):
    status: str
    model: str
    device: Optional[str] = None
