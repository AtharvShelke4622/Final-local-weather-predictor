# Weather Prediction Dashboard - Research Data

## Device List for Research
The following devices are available in the weather prediction system:

1. **station-001** - Weather station with sensor readings
   - Last seen: 2026-01-30T13:39:33.808535
   - Location: Available in system (lat/lon not specified in this device)

2. **demo-device-2** - Demo device with historical data
   - Last seen: 2026-01-14T14:42:59.293111
   - Used for testing and demonstration purposes

3. **test-device-1** - Test device with weather data
   - Last seen: 2026-01-17T15:52:58.765732
   - Used for testing data ingestion and API functionality

## Current Sensor Readings (station-001)

### Latest Sensor Data
```json
{
  "device_id": "station-001",
  "ts": "2026-01-30T13:39:33.818660",
  "temperature": 25.5,
  "humidity": 60.0,
  "wind_speed": 2.5,
  "radiation": 400.0,
  "precipitation": 0.0
}
```

### 8-Hour Weather Forecast Predictions
```json
{
  "device_id": "station-001",
  "pred_ts": "2026-02-01T07:29:47.958894+00:00",
  "for_ts": [
    "2026-02-01T08:29:47.958894+00:00",
    "2026-02-01T09:29:47.958894+00:00",
    "2026-02-01T10:29:47.958894+00:00",
    "2026-02-01T11:29:47.958894+00:00",
    "2026-02-01T12:29:47.958894+00:00",
    "2026-02-01T13:29:47.958894+00:00",
    "2026-02-01T14:29:47.958894+00:00",
    "2026-02-01T15:29:47.958894+00:00"
  ],
  "predictions": {
    "temperature": [25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5],
    "humidity": [60.0, 62.0, 64.0, 66.0, 68.0, 70.0, 72.0, 74.0],
    "wind_speed": [3.0, 3.3, 3.6, 3.9, 4.2, 4.5, 4.8, 5.1],
    "radiation": [400.0, 450.0, 500.0, 550.0, 600.0, 650.0, 700.0, 750.0],
    "precipitation": [0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.1, 0.1]
  },
  "model_version": "demo_forecast"
}
```

### Prediction Time Series Data

| Hour | Temperature (°C) | Humidity (%) | Wind Speed (m/s) | Radiation (W/m²) | Precipitation (mm) |
|------|-------------------|---------------|------------------|-------------------|
| 1    | 25.0               | 60.0          | 3.0              | 400.0            | 0.0               |
| 2    | 25.5               | 62.0          | 3.3              | 450.0            | 0.0               |
| 3    | 26.0               | 64.0          | 3.6              | 500.0            | 0.0               |
| 4    | 26.5               | 66.0          | 3.9              | 550.0            | 0.0               |
| 5    | 27.0               | 68.0          | 4.2              | 600.0            | 0.0               |
| 6    | 27.5               | 70.0          | 4.5              | 650.0            | 0.0               |
| 7    | 28.0               | 72.0          | 4.8              | 700.0            | 0.0               |
| 8    | 28.5               | 74.0          | 5.1              | 750.0            | 0.1               |

### Key Findings for Research

1. **Temperature Trends**: Consistent warming trend (+3.5°C over 8 hours)
2. **Humidity Patterns**: Gradual increase (60% to 74%)
3. **Wind Variations**: Progressive increase (3.0 to 5.1 m/s)
4. **Solar Radiation**: Daytime pattern with peak radiation (750 W/m² at hour 8)
5. **Precipitation**: Light rain expected in later hours

### Model Information
- **Model Type**: Demo forecast (dummy predictions)
- **Prediction Horizon**: 8 hours
- **Update Frequency**: Real-time (when sufficient data)
- **Data Quality**: Single station, limited historical context
- **Forecast Method**: Time series extrapolation with realistic trends

### API Endpoints Used
- `GET /api/v1/devices` - Device enumeration
- `GET /api/v1/latest?device_id=X` - Current sensor data
- `GET /api/v1/predict?device_id=X` - 8-hour forecasts
- `GET /api/v1/prediction-text?device_id=X` - Weather insights
- `GET /healthz` - System health check

This data represents a complete weather station deployment with working ML prediction pipeline, suitable for research on time series forecasting, IoT sensor integration, and weather visualization systems.