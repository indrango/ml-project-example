"""
RunPod Handler for YOLOv8 Object Detection API
Wraps the YOLO service directly for RunPod serverless deployment
"""

import runpod
import base64
from io import BytesIO
from PIL import Image
from app.services.yolo_service import get_yolo_service
from app.core.config import settings


def handler(event):
    """
    RunPod serverless handler for YOLOv8 object detection
    
    Expected input format:
    {
        "input": {
            "method": "predict" | "health",
            "image_base64": "base64_encoded_image_string" (for predict),
            "image_url": "https://..." (for predict, alternative to base64)
        }
    }
    """
    try:
        input_data = event.get("input", {})
        method = input_data.get("method", "predict")
        
        if method == "health":
            # Health check endpoint
            return {
                "status": "success",
                "data": {
                    "status": "ok",
                    "model": settings.model_name,
                    "device": settings.device
                }
            }
        
        elif method == "predict":
            # Image prediction endpoint
            image_base64 = input_data.get("image_base64")
            image_url = input_data.get("image_url")
            
            if not image_base64 and not image_url:
                return {
                    "status": "error",
                    "error": "Either image_base64 or image_url must be provided"
                }
            
            # Handle base64 image
            if image_base64:
                try:
                    # Decode base64 image
                    image_data = base64.b64decode(image_base64)
                    image = Image.open(BytesIO(image_data)).convert("RGB")
                    
                except Exception as e:
                    return {
                        "status": "error",
                        "error": f"Failed to decode base64 image: {str(e)}"
                    }
            
            # Handle image URL
            elif image_url:
                try:
                    import requests
                    response = requests.get(image_url, timeout=10)
                    response.raise_for_status()
                    image = Image.open(BytesIO(response.content)).convert("RGB")
                except Exception as e:
                    return {
                        "status": "error",
                        "error": f"Failed to download image from URL: {str(e)}"
                    }
            
            # Get service and run prediction
            try:
                service = get_yolo_service()
                detections = service.predict_image(image)
                
                return {
                    "status": "success",
                    "data": {
                        "model": service.model_name,
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
                    "error": f"Failed to run prediction: {str(e)}"
                }
        
        else:
            return {
                "status": "error",
                "error": f"Unknown method: {method}. Supported methods: 'predict', 'health'"
            }
    
    except Exception as e:
        return {
            "status": "error",
            "error": f"Handler error: {str(e)}"
        }


if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
