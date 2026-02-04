import requests
import json

BASE_URL = "http://localhost:5000"

# Step 1: Login
print("=== Testing AI Proctor Endpoints ===\n")
print("1. Logging in...")
login_response = requests.post(f"{BASE_URL}/api/candidate/login", json={
    "email": "john.doe@example.com",
    "password": "Password123!"
})

if login_response.status_code != 200:
    print(f"❌ Login failed: {login_response.status_code}")
    print(login_response.text)
    exit(1)

token = login_response.json().get('token')
print(f"✅ Logged in, token: {token[:30]}...")

# Step 2: Test Proctor Session Start
print("\n2. Starting proctoring session...")
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
session_response = requests.post(
    f"{BASE_URL}/api/proctor/session/start", 
    headers=headers,
    json={"assessment_id": "test-123"}
)

print(f"Status: {session_response.status_code}")
print(f"Response: {json.dumps(session_response.json(), indent=2)}")

if session_response.status_code == 200:
    session_data = session_response.json()
    if session_data.get('success'):
        session_id = session_data.get('session_id')
        print(f"✅ Session started: {session_id}")
        
        # Step 3: Test analyze-frame
        print("\n3. Testing frame analysis...")
        # Dummy base64 image (1x1 transparent PNG)
        dummy_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        
        analyze_response = requests.post(
            f"{BASE_URL}/api/proctor/analyze-frame",
            headers=headers,
            json={"session_id": session_id, "image": dummy_image}
        )
        
        print(f"Status: {analyze_response.status_code}")
        print(f"Response: {json.dumps(analyze_response.json(), indent=2)}")
        
        if analyze_response.status_code == 200:
            print("✅ Frame analysis working!")
        else:
            print("❌ Frame analysis failed")
    else:
        print("❌ Session start unsuccessful")
else:
    print("❌ Session start failed")
