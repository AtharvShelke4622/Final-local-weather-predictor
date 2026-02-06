#!/usr/bin/env python3
"""
Simple test data posting
"""
import requests
import json

def post_simple_data():
    base_url = "http://localhost:8002"
    
    # Get auth token first
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        print("Getting auth token...")
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            print("Got token!")
            
            # Simple device data
            device_data = {
                "device_id": "station-001",
                "temperature": 25.5,
                "humidity": 60.0,
                "wind_speed": 2.5,
                "radiation": 400.0,
                "precipitation": 0.0,
                "lat": 12.9716,
                "lon": 77.5946
            }
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            print("Posting device data...")
            response = requests.post(
                f"{base_url}/api/v1/ingest",
                json=device_data,
                headers=headers
            )
            
            print(f"Response: {response.status_code}")
            if response.status_code != 200:
                print(f"Error: {response.text}")
            else:
                print("Success! Data posted.")
                
                # Check devices list
                print("Checking devices...")
                response = requests.get(f"{base_url}/api/v1/devices", headers=headers)
                print(f"Devices: {response.json()}")
                
        else:
            print(f"Login failed: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    post_simple_data()