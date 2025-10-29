"""
Modal deployment file for YOLOv8 Object Detection API
Deploy with: modal deploy modal.py
"""

import modal

# Define the Docker image with all dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install(
        "libglib2.0-0",
        "libsm6",
        "libxrender1",
        "libxext6",
        "libgl1",
        "libgomp1"
    )
    .pip_install(
        "fastapi==0.115.2",
        "uvicorn[standard]==0.30.6",
        "pydantic==2.9.2",
        "python-multipart==0.0.9",
        "Pillow==10.4.0",
        "opencv-python-headless==4.10.0.84",
        "ultralytics==8.3.26",
        "numpy==1.26.4"
    )
)

# Create the Modal app
app = modal.App("yolov8-serving", image=image)

# Define the API endpoint with GPU support
@app.cls(
    gpu="A10G",  # Use A10G GPU for inference
    container_idle_timeout=300,  # Keep container alive for 5 minutes
    secrets=[],  # Add any secrets here if needed
)
class YOLOAPI:
    def __init__(self):
        """Initialize the YOLO model when the container starts"""
        from app.services.yolo_service import get_yolo_service
        self.service = get_yolo_service()

    @modal.method()
    def predict(self, image_bytes: bytes) -> dict:
        """
        Run object detection on an image
        
        Args:
            image_bytes: The image file as bytes
            
        Returns:
            dict: Detection results with bounding boxes and classes
        """
        from io import BytesIO
        from PIL import Image
        
        try:
            # Convert bytes to PIL Image
            image = Image.open(BytesIO(image_bytes)).convert("RGB")
            
            # Run prediction
            detections = self.service.predict_image(image)
            
            return {
                "status": "success",
                "data": {
                    "model": self.service.model_name,
                    "num_detections": len(detections),
                    "detections": [
                        {
                            "class_id": d.class_id,
                            "class_name": d.class_name,
                            "confidence": d.confidence,
                            "bbox": {
                                "x1": d.bbox.x1,
                                "y1": d.bbox.y1,
                                "x2": d.bbox.x2,
                                "y2": d.bbox.y2
                            }
                        }
                        for d in detections
                    ]
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    @modal.method()
    def health(self) -> dict:
        """Health check endpoint"""
        from app.core.config import settings
        
        return {
            "status": "ok",
            "model": settings.model_name,
            "device": settings.device
        }


# Expose the FastAPI app as a web endpoint
@app.function(
    image=image,
    allow_concurrent_inputs=10,
    container_idle_timeout=300,
)
@modal.asgi_app()
def fastapi_app():
    """Serve the FastAPI application"""
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from app.api.routes import router as api_router
    
    web_app = FastAPI(title="YOLOv8 Tiny Serving API", version="0.1.0")
    
    # Add CORS middleware
    web_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include the API router
    web_app.include_router(api_router, prefix="/api")
    
    @web_app.get("/")
    async def root():
        return {"message": "YOLOv8 Tiny model serving is running", "docs": "/docs"}
    
    return web_app

