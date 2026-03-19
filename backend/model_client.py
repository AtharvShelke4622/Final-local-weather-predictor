import httpx
import random
from datetime import datetime, timedelta, timezone
from typing import List
from app_config import settings

TARGETS = ["temperature", "humidity", "wind_speed", "radiation", "precipitation"]

async def predict_8h(device_id: str, recent_window: List[List[float]]):
    if len(recent_window) != 24:
        raise ValueError("recent_window must contain exactly 24 rows")

    url = f"{settings.MODEL_SERVER_URL}/model/predict"
    payload = {
        "device_id": device_id,
        "recent_window": recent_window,
    }

    async with httpx.AsyncClient(timeout=15) as client:
        try:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()

            preds = data["predictions_8h"]
            model_version = data["model_version"]

        except Exception as e:
            # HARD fallback (model server unreachable)
            last = recent_window[-1]
            preds = {
                "temperature": [float(last[0]) + 0.15 * step for step in range(8)],
                "humidity": [float(last[1]) + random.uniform(-0.6, 0.6) * step for step in range(8)],
                "wind_speed": [max(0, float(last[2]) + 0.2 * step) for step in range(8)],
                "radiation": [max(0, float(last[3]) + 50 * step) for step in range(8)],
                "precipitation": [max(0, float(last[4]) + 0.02 * step) for step in range(8)],
            }
            model_version = "fallback"

    now = datetime.now(timezone.utc)
    for_ts = [
        (now + timedelta(hours=i + 1)).isoformat()
        for i in range(8)
    ]

    return for_ts, preds, model_version
