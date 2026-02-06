#!/usr/bin/env python3
"""
Simple backend with working predict endpoint
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, timezone, timedelta
import uvicorn

app = FastAPI(title="Simple Weather API")

# Sample data
devices = [
    {"device_id": "station-001", "last_seen": "2026-01-30T13:39:33.808535"},
    {"device_id": "demo-device-2", "last_seen": "2026-01-14T14:42:59.293111"},
    {"device_id": "test-device-1", "last_seen": "2026-01-17T15:52:58.765732"}
]

class LatestOut(BaseModel):
    device_id: str
    ts: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    radiation: Optional[float] = None
    precipitation: Optional[float] = None

class ForecastOut(BaseModel):
    device_id: str
    pred_ts: str
    for_ts: List[str]
    predictions: Dict[str, List[float]]
    model_version: str

# Sample latest readings
latest_readings = {
    "station-001": {
        "device_id": "station-001",
        "ts": "2026-01-30T13:39:33.818660",
        "temperature": 25.5,
        "humidity": 60.0,
        "wind_speed": 2.5,
        "radiation": 400.0,
        "precipitation": 0.0
    }
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Simple Weather API"}

@app.get("/api/v1/devices")
async def get_devices():
    """Public devices endpoint - returns actual device list"""
    return devices

@app.get("/api/v1/latest")
async def get_latest(device_id: str):
    """Public latest endpoint"""
    return latest_readings.get(device_id)

@app.get("/api/v1/predict")
async def get_predict(device_id: str):
    """Public predict endpoint with dummy data"""
    # Generate 8-hour dummy forecast
    base_temp = 25.0
    base_humidity = 60.0
    
    dummy_predictions = {
        "temperature": [base_temp + i * 0.5 for i in range(8)],
        "humidity": [base_humidity + i * 2 for i in range(8)],
        "wind_speed": [3.0 + i * 0.3 for i in range(8)],
        "radiation": [400.0 + i * 50 for i in range(8)],
        "precipitation": [0.1 if i > 4 else 0.0 for i in range(8)]
    }
    
    # Generate timestamps
    for_ts = []
    base_time = datetime.now(timezone.utc)
    for i in range(8):
        for_ts.append((base_time + timedelta(hours=i+1)).isoformat())
    
    return {
        "device_id": device_id,
        "pred_ts": base_time.isoformat(),
        "for_ts": for_ts,
        "predictions": dummy_predictions,
        "model_version": "demo_forecast",
    }

@app.get("/api/v1/prediction-text")
async def get_prediction_text(device_id: str):
    """Public prediction text endpoint"""
    return {
        "device_id": device_id,
        "model_version": "demo",
        "generated_at": datetime.now(timezone.utc),
        "prediction_text": {
            "summary": ["Weather data available for analysis"],
            "trend": ["Temperature patterns consistent with seasonal expectations"]
        }
    }

@app.get("/healthz")
async def healthz():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)