# YOLOv8 Tiny Model Serving (FastAPI)

Serve Ultralytics YOLOv8 nano ("tiny") with FastAPI. Includes Docker setup for deployment to common model serving platforms.

## Features
- Health and prediction endpoints
- Loads `yolov8n.pt` by default (configurable)
- Single-process service with lazy singleton model
- Dockerfile for CPU serving

## Quickstart (Local)

```bash
# Create venv (optional)
python3 -m venv .venv && source .venv/bin/activate

# Install deps
pip install -r requirements.txt

# Run API
uvicorn app.main:app --reload --port 8000
```

Open docs at `http://localhost:8000/docs`.

## Endpoints
- GET `/` – basic info
- GET `/api/health` – service health
- POST `/api/predict` – multipart form with `file` image

Example (curl):
```bash
curl -s -X POST "http://localhost:8000/api/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/image.jpg"
```

Response:
```json
{
  "model": "yolov8n.pt",
  "num_detections": 2,
  "detections": [
    {
      "class_id": 0,
      "class_name": "person",
      "confidence": 0.84,
      "bbox": {"x1": 12.3, "y1": 45.6, "x2": 100.1, "y2": 200.2}
    }
  ]
}
```

## Configuration
Environment variables:
- `MODEL_NAME` (default: `yolov8n.pt`)
- `DEVICE` (e.g., `cpu`, `cuda` if GPU available in env)
- `CONF_THRESHOLD` (default: `0.25`)
- `IOU_THRESHOLD` (default: `0.45`)
- `MAX_DETECTIONS` (default: `300`)

## Docker

### Build and Run
```bash
docker build -t yolo-serving .
docker run --rm -p 8000:8000 -e MODEL_NAME=yolov8n.pt yolo-serving
```

### Docker Optimizations
- Multi-stage build separates build tools from runtime image
- Pip cache mount reduces rebuild time significantly
- Staged dependency installation reduces peak memory usage
- Final image excludes build-essential (smaller size)
- Optimized for cloud platforms like DigitalOcean App Platform
- Build completes in ~2-3 minutes with ~1-2GB memory usage

## Modal Deployment

### Quick Deploy to Modal

1. **Install Modal CLI**:
```bash
pip install modal
```

2. **Authenticate**:
```bash
modal token new
```

3. **Deploy**:
```bash
modal deploy modal.py
```

4. **Test the endpoint**:
```bash
curl https://<your-app>.modal.run/api/health
```

### Features
- ✅ GPU-accelerated inference (A10G GPU)
- ✅ Auto-scaling based on traffic
- ✅ Pay-per-use pricing
- ✅ Fast cold starts
- ✅ HTTPS endpoint included

### Documentation
See [MODAL_DEPLOYMENT.md](MODAL_DEPLOYMENT.md) for detailed deployment guide.

## Notes
- First request triggers model download if not present; cache persists in the container layer.
- For GPU serving, use a CUDA-enabled base image and set `DEVICE=cuda` if your platform provides GPUs.
