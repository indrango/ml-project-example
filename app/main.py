from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router

app = FastAPI(title="YOLOv8 Tiny Serving API", version="0.1.0")

# Basic CORS setup for model serving platforms
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome, YOLOv8 Tiny model serving is running", "docs": "/docs"}
