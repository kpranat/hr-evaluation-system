import requests
import json

# Test MCQ endpoint
BASE_URL = "http://localhost:5000"

# Get a valid token (you'll need to login first)
login_data = {
    "email": "john.doe@example.com",
    "password": "Password123!"
}

print("🔐 Logging in...")
login_response = requests.post(f"{BASE_URL}/api/candidate/login", json=login_data)
print(f"Login Status: {login_response.status_code}")

if login_response.status_code == 200:
    login_json = login_response.json()
    token = login_json.get('token')
    print(f"✅ Token received: {token[:20]}..." if token else "❌ No token in response")
    
    # Test MCQ questions endpoint
    print("\n📚 Fetching MCQ questions...")
    headers = {"Authorization": f"Bearer {token}"}
    mcq_response = requests.get(f"{BASE_URL}/api/mcq/questions", headers=headers)
    
    print(f"MCQ Endpoint Status: {mcq_response.status_code}")
    print(f"Response Headers: {dict(mcq_response.headers)}")
    
    if mcq_response.status_code == 200:
        mcq_data = mcq_response.json()
        print(f"\n✅ Success! Received data:")
        print(json.dumps(mcq_data, indent=2)[:500])
        
        if 'questions' in mcq_data:
            print(f"\n📊 Total questions: {len(mcq_data['questions'])}")
            if mcq_data['questions']:
                first_q = mcq_data['questions'][0]
                print(f"\n🔍 First question structure:")
                print(json.dumps(first_q, indent=2))
    else:
        print(f"❌ Error: {mcq_response.text}")
else:
    print(f"❌ Login failed: {login_response.text}")
