from fastapi import FastAPI, Depends, BackgroundTasks, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, AsyncGenerator
from datetime import datetime, timezone
from sqlalchemy import select
from logging_config import logger, audit_logger, setup_logging, error_boundary, database_transaction
from app_config import settings
from database import AsyncSessionLocal, init_models, ping_db
import crud
from schemas import IngestPayload, DeviceOut, LatestOut, ForecastOut
from model_client import predict_8h
from db_models import Device, SensorReading, User
from prediction_text import generate_prediction_text
from auth_routes import router as auth_router
from auth import get_current_active_user, user_required
from rate_limiter import limiter, rate_limit_exceeded_handler
# Cache is disabled for now
# cache = None
from metrics import metrics_endpoint

# Configure structured logging
import structlog
logger = structlog.get_logger()

app = FastAPI(
    title=settings.APP_NAME,
    description="Local Weather Prediction Dashboard API",
    version="2.0.0"
)

# =========================================================
# RATE LIMITING
# =========================================================
app.state.limiter = limiter
app.add_exception_handler(429, rate_limit_exceeded_handler)

# =========================================================
# CORS
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# DB SESSION
# =========================================================
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# =========================================================
# INCLUDE ROUTES
# =========================================================
app.include_router(auth_router)

# =========================================================
# STARTUP
# =========================================================
@app.on_event("startup")
async def on_startup():
    setup_logging()
    await init_models()
    await ping_db()
    logger.info("Application started successfully")
    audit_logger.log_system_event(
        event_type="application_startup",
        severity="info",
        component="main_api",
        details={"version": "2.0.0"}
    )

# =========================================================
# SHUTDOWN
# =========================================================
@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Application shutdown complete")

# =========================================================
# HEALTH
# =========================================================
@app.get("/healthz")
@limiter.limit("100/minute")
async def healthz(request: Request):
    return {"status": "ok", "timestamp": datetime.now(timezone.utc)}



# =========================================================
# METRICS
# =========================================================
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return await metrics_endpoint()

# =========================================================
# PUBLIC ENDPOINTS (for frontend without auth)
# =========================================================
@app.get("/api/v1/devices", response_model=List[DeviceOut])
async def devices_public():
    """Public devices endpoint - returns actual device list"""
    async with AsyncSessionLocal() as session:
        items = await crud.list_devices(session)
        return [DeviceOut(**i) for i in items]

@app.get("/api/v1/latest", response_model=Optional[LatestOut])
async def latest_public(device_id: str = Query(...)):
    """Public latest endpoint"""
    async with AsyncSessionLocal() as session:
        return await crud.get_latest_reading(session, device_id)

@app.get("/api/v1/predict", response_model=Optional[ForecastOut])
async def predict_public(device_id: str = Query(...)):
    """Public predict endpoint - provides dummy forecasts when insufficient data"""
    async with AsyncSessionLocal() as session:
        window = await crud.last_n_readings(session, device_id, n=24)
        
        if not window or len(window) < 24:
            # Return dummy predictions when insufficient data
            last_reading = await crud.get_latest_reading(session, device_id)
            if last_reading:
# Generate 8-hour dummy forecast based on last reading
            last_reading = await crud.get_latest_reading(session, device_id)
            if last_reading:
                # Generate 8-hour dummy forecast based on last reading
                base_temp = getattr(last_reading, 'temperature', 25.0)
                base_humidity = getattr(last_reading, 'humidity', 60.0)
                
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
            else:
                return {
                    "device_id": device_id,
                    "pred_ts": datetime.now(timezone.utc),
                    "for_ts": [],
                    "predictions": {},
                    "model_version": "no_data",
                }
        
        try:
            from model_client import predict_8h
            for_ts, preds, model_version = await predict_8h(device_id, window)
            return {
                "device_id": device_id,
                "pred_ts": datetime.now(timezone.utc),
                "for_ts": for_ts,
                "predictions": preds,
                "model_version": model_version,
            }
        except Exception as e:
            print(f"Prediction error for {device_id}: {e}")
            return {
                "device_id": device_id,
                "pred_ts": datetime.now(timezone.utc),
                "for_ts": [],
                "predictions": {},
                "model_version": f"error: {str(e)}",
            }

@app.get("/api/v1/prediction-text")
async def prediction_text_public(device_id: str = Query(...)):
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

# =========================================================
# INGEST
# =========================================================
@app.post("/api/v1/ingest")
@limiter.limit("60/minute")
@error_boundary
async def ingest(
    request: Request,
    payload: IngestPayload,
    bg: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(user_required),
):
    device = await crud.upsert_device(
        session,
        payload.device_id,
        payload.lat,
        payload.lon,
    )

    reading = SensorReading(
        device_id=device.id,
        device_key=device.device_id,
        ts=payload.ts or datetime.now(timezone.utc),
        temperature=payload.temperature,
        humidity=payload.humidity,
        wind_speed=payload.wind_speed,
        radiation=payload.radiation,
        precipitation=payload.precipitation,
        raw=payload.model_dump(),
    )

    async with database_transaction(session, "ingest_sensor_reading"):
        session.add(reading)
        await session.flush()
        
        # Log data access
        audit_logger.log_data_access(
            user_id=current_user.id,
            resource_type="sensor_reading",
            resource_id=payload.device_id,
            action="create",
            ip_address=request.client.host if request.client else "unknown",
            details={"payload": payload.dict()}
        )

    async def _bg_task(dev_id: str):
        async with AsyncSessionLocal() as s:
            window = await crud.last_n_readings(s, dev_id, n=24)

            if not window:
                return

            for_ts, preds, model_version = await predict_8h(dev_id, window)

            result = await s.execute(
                select(Device).where(Device.device_id == dev_id)
            )
            dev = result.scalar_one_or_none()

            if dev:
                await crud.store_forecast(
                    s,
                    dev,
                    for_ts,
                    preds,
                    model_version,
                )
                await s.commit()

    bg.add_task(_bg_task, payload.device_id)
    return {"status": "ingested"}

# =========================================================
# LATEST
# =========================================================
@app.get("/api/v1/latest", response_model=Optional[LatestOut])
@limiter.limit("100/minute")
async def latest(
    request: Request,
    device_id: str = Query(...),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(user_required),
):
    return await crud.get_latest_reading(session, device_id)

# =========================================================
# DEVICES
# =========================================================
@app.get("/api/v1/devices", response_model=List[DeviceOut])
@limiter.limit("50/minute")
async def devices(
    request: Request,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(user_required),
):
    items = await crud.list_devices(session)
    return [DeviceOut(**i) for i in items]

# =========================================================
# NUMERIC FORECAST
# =========================================================
@app.get("/api/v1/predict", response_model=Optional[ForecastOut])
@limiter.limit("30/minute")
async def predict(
    request: Request,
    device_id: str = Query(...),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(user_required),
):
    window = await crud.last_n_readings(session, device_id, n=24)

    if not window:
        return {
            "device_id": device_id,
            "pred_ts": datetime.now(timezone.utc),
            "for_ts": [],
            "predictions": {},
            "model_version": "fallback",
        }

    for_ts, preds, model_version = await predict_8h(device_id, window)

    result = await session.execute(
        select(Device).where(Device.device_id == device_id)
    )
    dev = result.scalar_one_or_none()

    if not dev:
        return None

    await crud.store_forecast(
        session,
        dev,
        for_ts,
        preds,
        model_version,
    )
    await session.commit()

    return {
        "device_id": device_id,
        "pred_ts": datetime.now(timezone.utc),
        "for_ts": for_ts,
        "predictions": preds,
        "model_version": model_version,
    }

# =========================================================
# HUMAN READABLE TEXT
# =========================================================
@app.get("/api/v1/prediction-text")
@limiter.limit("30/minute")
async def prediction_text(
    request: Request,
    device_id: str = Query(...),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(user_required),
):
    window = await crud.last_n_readings(session, device_id, n=24)

    if not window:
        return {
            "device_id": device_id,
            "status": "insufficient_data",
            "message": "At least one sensor reading is required.",
            "prediction_text": {},
        }

    for_ts, preds, model_version = await predict_8h(device_id, window)
    readable_text = generate_prediction_text(preds)

    return {
        "device_id": device_id,
        "model_version": model_version,
        "generated_at": datetime.now(timezone.utc),
        "prediction_text": readable_text,
    }
