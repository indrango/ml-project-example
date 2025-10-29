# Quick Start: Deploy to Modal - Step by Step

## Overview
Deploy your YOLOv8 Object Detection API to Modal with GPU acceleration in minutes.

## Prerequisites
- Python 3.11+ installed
- A Modal account (free tier available)
- Git (for version control)

---

## Step-by-Step Deployment

### Step 1: Checkout the Branch
```bash
git checkout modal-deployment
git pull origin modal-deployment
```

### Step 2: Install Modal CLI
```bash
# Create/activate virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Modal
pip install modal

# Or install all requirements
pip install -r modal_requirements.txt
```

### Step 3: Authenticate with Modal
```bash
# Run authentication command
modal token new
```

This will:
1. Open your browser
2. Log you into Modal
3. Save your authentication token locally

### Step 4: Review Configuration (Optional)

Open `modal.py` to review settings:
- **GPU Type**: Currently set to `A10G` (can change to T4, A100, etc.)
- **Model**: Currently `yolov8n.pt` 
- **Timeout**: 300 seconds (5 minutes)

### Step 5: Deploy to Modal
```bash
# Deploy the application
modal deploy modal.py
```

**What happens during deployment:**
1. Modal builds a Docker image with your dependencies
2. Uploads it to Modal's registry
3. Creates serverless endpoints
4. Shows you the deployment URL

**Expected output:**
```
✓ Initialized. View deployment at: https://modal.com/apps/<app-name>
✓ Created objects.
✓ App deployed successfully!

┌─────────────────────────────────────────────────────────────┐
│ App: https://modal.com/apps/<app-name>                      │
│ Web: https://<app-name>--<user>--fastapi-app.modal.run     │
└─────────────────────────────────────────────────────────────┘
```

### Step 6: Test Your Deployment

#### A. Test Health Endpoint
```bash
curl https://<your-app-url>/api/health
```

Expected response:
```json
{"status":"ok","model":"yolov8n.pt","device":"cuda"}
```

#### B. Test Prediction Endpoint
```bash
# Using curl with a test image URL
curl -X POST https://<your-app-url>/api/predict \
  -F "file=@path/to/image.jpg"
```

Or use the provided test script:
```bash
python test_modal.py https://<your-app-url>
```

#### C. View Interactive API Documentation
Open in browser: `https://<your-app-url>/docs`

### Step 7: Monitor Your Deployment

#### View in Dashboard
```bash
# Open Modal dashboard
modal dashboard
```

Or visit: https://modal.com/apps

#### View Logs
```bash
# View real-time logs
modal app logs <app-name>
```

---

## What You Get

✅ **HTTPS API Endpoint** - Secure, public URL for your API  
✅ **GPU Acceleration** - A10G GPU for fast inference  
✅ **Auto-scaling** - Automatically handles traffic spikes  
✅ **Pay-per-use** - Only pay for actual usage  
✅ **Fast Deploys** - Updates deploy in seconds  
✅ **Monitoring** - Built-in logs and metrics  

---

## Common Tasks

### Update Your Deployment
```bash
# Make changes to your code, then:
modal deploy modal.py
```

### Change GPU Type
Edit `modal.py` line 39:
```python
gpu="T4",  # Change from A10G to T4, A100, etc.
```

### Stop Your Deployment
```bash
modal app stop <app-name>
```

### View Costs
Visit https://modal.com/account/billing

---

## Troubleshooting

### Issue: "modal: command not found"
**Solution:** Install Modal: `pip install modal`

### Issue: Authentication failed
**Solution:** Run `modal token new` again

### Issue: "Module not found" error
**Solution:** Check that all dependencies are in `modal.py` image definition

### Issue: Cold start too slow
**Solution:** Increase `container_idle_timeout` in `modal.py`

---

## Next Steps

1. **Customize the Model**
   - Change MODEL_NAME environment variable
   - Try different YOLOv8 models (yolov8s.pt, yolov8m.pt, etc.)

2. **Add Authentication**
   - Set up API keys
   - Add middleware for auth

3. **Integrate with Your App**
   - Use the API endpoint in your application
   - Set up webhooks

4. **Monitor Performance**
   - Set up alerts
   - Track usage metrics

---

## Files Overview

- **modal.py** - Main deployment configuration
- **modal_requirements.txt** - Modal-specific dependencies
- **test_modal.py** - Test script for endpoints
- **MODAL_DEPLOYMENT.md** - Detailed deployment guide
- **DEPLOY_MODAL.md** - This quick start guide

---

## Support

- **Modal Docs**: https://modal.com/docs
- **GitHub Issues**: https://github.com/indrango/ml-project-example/issues
- **Modal Support**: support@modal.com

---

## Ready to Deploy?

```bash
# Quick deploy command
modal deploy modal.py
```

That's it! Your YOLOv8 API is now live on Modal with GPU acceleration! 🚀

