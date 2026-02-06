#!/usr/bin/env python3
"""
Generate and post test weather data to the API
"""
import requests
import json
from datetime import datetime, timedelta
import random

def generate_test_data():
    base_url = "http://localhost:8002"
    
    # Generate realistic weather data for multiple devices
    devices = [
        {
            "device_id": "station-001",
            "lat": 12.9716,
            "lon": 77.5946
        },
        {
            "device_id": "station-002", 
            "lat": 28.6139,
            "lon": 77.2090
        },
        {
            "device_id": "station-003",
            "lat": 19.0760,
            "lon": 72.8777
        }
    ]
    
    print("Generating Test Weather Data")
    print("=" * 50)
    
    for device in devices:
        print(f"\nProcessing device: {device['device_id']}")
        
        # Generate 24 hours of data (one reading every hour)
        base_temp = random.uniform(20, 30)
        base_humidity = random.uniform(50, 80)
        
        for i in range(24):
            # Create realistic variations
            hour_variation = math.sin(i * math.pi / 12) * 5  # Daily temperature cycle
            
            timestamp = datetime.now() - timedelta(hours=24-i)
            
            data = {
                "device_id": device["device_id"],
                "ts": timestamp.isoformat() + "Z",
                "temperature": round(base_temp + hour_variation + random.uniform(-2, 2), 1),
                "humidity": round(base_humidity + random.uniform(-10, 10), 1),
                "wind_speed": round(random.uniform(0, 15), 1),
                "radiation": round(random.uniform(0, 1000), 0) if 6 <= i <= 18 else 0,
                "precipitation": round(random.uniform(0, 5), 1) if random.random() < 0.2 else 0.0,
                "lat": device["lat"],
                "lon": device["lon"]
            }
            
            # Post data to API
            try:
                response = requests.post(
                    f"{base_url}/api/v1/ingest",
                    json=data,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                if response.status_code == 200:
                    print(f"  [OK] Hour {i+1}: {data['temperature']}C, {data['humidity']}% - Posted successfully")
                else:
                    print(f"  [FAIL] Hour {i+1}: Failed - {response.status_code} - {response.text}")
            except Exception as e:
                print(f"  [ERROR] Hour {i+1}: Error - {e}")
            
            # Small delay to avoid overwhelming the API
            time.sleep(0.1)
    
    print(f"\nTest data generation complete!")
    print(f"Check the dashboard at: http://localhost:5173")
    print(f"You should now see {len(devices)} devices with sensor data")

if __name__ == "__main__":
    import math
    import time
    generate_test_data()