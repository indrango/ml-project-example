# Alternative using ultralytics/ultralytics:cpu base image
# Compare this with Dockerfile to see which works better

FROM ultralytics/ultralytics:latest-cpu

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_NAME=yolov8n.pt \
    UVICORN_WORKERS=1 \
    PORT=8000

WORKDIR /app

# Install FastAPI and uvicorn (ultralytics base image already has PyTorch, ultralytics, etc.)
RUN pip install --no-cache-dir \
    fastapi==0.115.2 \
    "uvicorn[standard]==0.30.6" \
    pydantic==2.9.2 \
    python-multipart==0.0.9

# Copy application code
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]