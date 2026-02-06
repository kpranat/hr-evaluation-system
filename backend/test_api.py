
import sys
import os
import json
import requests

# Get a valid recruiter token first
def get_token():
    response = requests.post("http://localhost:5000/recruiter-dashboard/login", json={
        "email": "admin@hreval.com",
        "password": "Admin123!"
    })
    if response.status_code == 200:
        data = response.json()
        return data.get("token")
    else:
        print(f"Login failed: {response.text}")
        return None

def test_candidate_detail(candidate_id=41):
    token = get_token()
    if not token:
        print("❌ Could not get token")
        return
    
    print(f"🔑 Got token: {token[:20]}...")
    
    # Call the candidate detail endpoint
    response = requests.get(f"http://localhost:5000/recruiter-dashboard/candidates/{candidate_id}", headers={
        "Authorization": f"Bearer {token}"
    })
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            candidate = data["candidate"]
            print(f"\n📊 Candidate {candidate_id} Response:")
            print(f"   Soft Skill Score: {candidate.get('soft_skill_score')}")
            print(f"   Fairplay Score: {candidate.get('fairplay_score')}")
            print(f"   Technical Score: {candidate.get('technical_score')}")
            print(f"   Integrity Logs Count: {len(candidate.get('integrity_logs', []))}")
            
            # Print first few logs
            logs = candidate.get('integrity_logs', [])[:3]
            for log in logs:
                print(f"   Log: {log}")
        else:
            print(f"❌ API Error: {data.get('message')}")
    else:
        print(f"❌ HTTP Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    test_candidate_detail()
