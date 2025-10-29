# syntax=docker/dockerfile:1

FROM pytorch/pytorch:2.9.0-cpu

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_NAME=yolov8n.pt \
    UVICORN_WORKERS=1 \
    PORT=8000

WORKDIR /app

# Install system dependencies in a single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgl1 \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (torch is already in base image)
RUN pip install --no-cache-dir \
    fastapi==0.115.2 \
    uvicorn[standard]==0.30.6 \
    pydantic==2.9.2 \
    python-multipart==0.0.9 \
    Pillow==10.4.0 \
    opencv-python-headless==4.10.0.84 \
    ultralytics==8.3.26 \
    numpy==1.26.4

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
