import os
import sys
import json

# Add backend directory to sys.path to enable local imports during test run
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "propgrowth", "backend")
sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    print("Health Check Response:", response.status_code, response.json())
    assert response.status_code == 200

def test_telemetry():
    response = client.get("/api/telemetry")
    print("Initial Telemetry Response:", response.status_code, response.json())
    assert response.status_code == 200

def test_full_flow():
    # Start analysis
    payload = {
        "address": "Whitefield, Bangalore",
        "city": "Bangalore",
        "budget_lakhs": 150.0,
        "bhk_type": "3BHK",
        "investment_horizon_years": 5
    }
    response = client.post("/api/analyze/start", json=payload)
    print("Start Analysis Response Status:", response.status_code)
    start_data = response.json()
    print("Start Analysis Response Keys:", list(start_data.keys()))
    
    # We support both agent.py structure and fallback structures
    thread_id = start_data.get("thread_id")
    assert thread_id is not None
    
    # Check status polling route
    response = client.get(f"/api/analyze/status/{thread_id}")
    print("Status Route Response:", response.status_code, response.json())
    assert response.status_code == 200
    
    # Extract comps for resuming
    report_dict = start_data.get("preliminary_report") or start_data
    comps = report_dict.get("comps") or []
    approved_comps = [c["id"] for c in comps[:2]] if comps else []
    
    # Resume analysis
    resume_payload = {
        "thread_id": thread_id,
        "approved_comps": approved_comps,
        "analyst_notes": "Strong tech hub growth, high appreciation potential."
    }
    response = client.post("/api/analyze/resume", json=resume_payload)
    print("Resume Analysis Response Status:", response.status_code)
    resume_data = response.json()
    print("Resume Analysis Response Keys:", list(resume_data.keys()))
    
    # Verify final report or status
    report_body = resume_data.get("report") or resume_data
    print("Final Growth Verdict:", report_body.get("growth_verdict") or resume_data.get("verdict"))
    
    # Get telemetry again to verify updates
    response = client.get("/api/telemetry")
    print("Final Telemetry Summary:")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    # Prevent unicode console output crash on Windows
    os.environ["PYTHONIOENCODING"] = "utf-8"
    
    print("--- 1. Testing FastAPI Health Route ---")
    test_health()
    print("\n--- 2. Testing FastAPI Telemetry Route ---")
    test_telemetry()
    print("\n--- 3. Testing FastAPI Analysis Flow Routes ---")
    test_full_flow()
