# Modal Deployment Guide for YOLOv8 Object Detection API

This guide walks you through deploying the YOLOv8 Object Detection API on Modal.

## Prerequisites

1. **Python 3.11+** installed locally
2. **Modal account** - sign up at [modal.com](https://modal.com)
3. **Modal CLI** installed

## Step 1: Install Modal CLI

```bash
# Install Modal CLI
pip install modal

# Or use the provided requirements
pip install -r modal_requirements.txt
```

## Step 2: Authenticate with Modal

```bash
# Login to Modal
modal token new
```

Follow the browser prompt to authenticate.

## Step 3: Review Configuration

Check `modal.py` for deployment settings:

- **GPU**: A10G (can be changed to T4, A100, etc.)
- **Container idle timeout**: 300 seconds (5 minutes)
- **Model**: yolov8n.pt (configurable via environment variable)

## Step 4: Deploy to Modal

### Option A: Deploy with FastAPI web endpoint (Recommended)

```bash
# Deploy the full application
modal deploy modal.py
```

This deploys the FastAPI app with all endpoints available.

### Option B: Deploy as a standalone function

```bash
# Deploy just the prediction function
modal deploy modal.py --class YOLOAPI
```

## Step 5: Get Your Endpoint URL

After deployment, Modal will show you the endpoint URL:

```
✓ Initialized. View deployment at: https://modal.com/apps/<your-app-name>
✓ App deployed successfully!

┌─────────────────────────────────────────────────────────────┐
│ App: https://modal.com/apps/<your-app-name>                 │
│ Web: https://<your-app>.modal.run                           │
└─────────────────────────────────────────────────────────────┘
```

## Step 6: Test the Deployment

### Test Health Endpoint

```bash
curl https://<your-app>.modal.run/api/health
```

Expected response:
```json
{
  "status": "ok",
  "model": "yolov8n.pt",
  "device": "cuda"
}
```

### Test Prediction Endpoint

```bash
# Using a local image file
curl -X POST https://<your-app>.modal.run/api/predict \
  -F "file=@/path/to/your/image.jpg"
```

Expected response:
```json
{
  "model": "yolov8n.pt",
  "num_detections": 3,
  "detections": [
    {
      "class_id": 0,
      "class_name": "person",
      "confidence": 0.84,
      "bbox": {"x1": 123.4, "y1": 45.6, "x2": 234.5, "y2": 167.8}
    }
  ]
}
```

### Using Python SDK

```python
import modal

# Initialize Modal client
stub = modal.App.lookup("<your-app-name>", "modal")

# Get the prediction function
predict = stub.function("predict")

# Load an image
with open("image.jpg", "rb") as f:
    image_bytes = f.read()

# Run prediction
result = predict(image_bytes)
print(result)
```

## Step 7: View Deployment Status

```bash
# List all apps
modal app list

# View app details
modal app show <your-app-name>

# View logs
modal app logs <your-app-name>
```

## Configuration Options

### Change GPU Type

Edit `modal.py`:

```python
@app.cls(
    gpu="T4",  # Change from A10G to T4, A100, etc.
    ...
)
```

Available GPU options:
- `"T4"` - Cheaper, good for testing
- `"A10G"` - Balanced performance
- `"A100"` - Best performance

### Change Model

Set environment variable in `modal.py`:

```python
image = image.env({"MODEL_NAME": "yolov8s.pt"})
```

Or modify `app/core/config.py` default.

### Adjust Container Settings

```python
@app.cls(
    gpu="A10G",
    container_idle_timeout=600,  # Keep alive for 10 minutes
    memory=8192,  # 8GB memory
    cpu=2,  # 2 CPUs
)
```

## Troubleshooting

### Issue: "Module not found"

**Solution**: Ensure all dependencies are in the `image` definition in `modal.py`

### Issue: "CUDA out of memory"

**Solution**: 
1. Reduce batch size in the code
2. Use a smaller model (yolov8n.pt)
3. Increase GPU memory

### Issue: Slow cold starts

**Solution**:
1. Increase `container_idle_timeout`
2. Use a smaller model
3. Deploy to a region closer to your users

## Monitoring

Monitor your deployment in the Modal dashboard:

```bash
# Open the Modal dashboard
modal dashboard
```

Or visit: https://modal.com/apps

## Cost Optimization

1. **Use cheaper GPU for testing**: T4 instead of A10G
2. **Reduce idle timeout**: If requests are infrequent
3. **Use CPU for simple tasks**: Remove GPU requirement for health checks
4. **Monitor usage**: Check Modal dashboard for actual costs

## Cleanup

To stop the deployment:

```bash
# Stop the app
modal app stop <your-app-name>

# Delete the app
-name>
```

## Next Steps

- Set up custom domain
- Add authentication
- Configure rate limiting
- Set up monitoring and alerts
- Integrate with your application

For more information, visit [Modal Documentation](https://modal.com/docs).

