from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from PIL import Image

from app.core.config import settings
from app.schemas import HealthResponse, PredictResponse
from app.services.yolo_service import YOLOService, get_yolo_service

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", model=settings.model_name, device=settings.device)


@router.post("/predict", response_model=PredictResponse)
async def predict(
    file: Annotated[UploadFile, File(description="Image file")],
    service: YOLOService = Depends(get_yolo_service),
) -> PredictResponse:
    try:
        image = Image.open(file.file).convert("RGB")
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=f"Invalid image: {exc}") from exc

    detections = service.predict_image(image)
    return PredictResponse(
        model=service.model_name,
        num_detections=len(detections),
        detections=detections,
    )
