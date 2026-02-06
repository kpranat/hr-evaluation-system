
import os
import sys
from pprint import pprint

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import CandidateAuth, MCQResult, PsychometricResult, TextAssessmentResult, CandidateRationale

def inspect_db():
    app = create_app()
    with app.app_context():
        print("✅ DB Connected successfully")
        
        # 1. Count Candidates
        count = CandidateAuth.query.count()
        print(f"📊 Total Candidates: {count}")
        
        if count == 0:
            print("❌ No candidates found in database!")
            return

        # 2. Inspect Candidate 1
        candidate_id = 1
        candidate = CandidateAuth.query.get(candidate_id)
        
        if not candidate:
            print(f"❌ Candidate {candidate_id} not found!")
            # Try to get first candidate
            candidate = CandidateAuth.query.first()
            print(f"ℹ️ Inspecting first available candidate (ID: {candidate.id}) instead...")
        else:
            print(f"ℹ️ Inspecting Candidate {candidate_id}...")
            
        print("\n--- Candidate Profile ---")
        print(f"ID: {candidate.id}")
        print(f"Email: {candidate.email}")
        print(f"Resume URL: {candidate.resume_url}")
        print(f"Resume Data Present: {bool(candidate.resume_data)}")
        if candidate.resume_data:
            print("Resume Data Keys:", candidate.resume_data.keys())
            
        print("\n--- Assessment Status ---")
        print(f"MCQ Completed: {candidate.mcq_completed}")
        print(f"Psychometric Completed: {candidate.psychometric_completed}")
        print(f"Technical Completed: {candidate.technical_completed}")
        
        print("\n--- Related Records ---")
        print(f"MCQ Result: {'✅ Found' if candidate.mcq_result else '❌ Missing'}")
        if candidate.mcq_result:
            print(f"  - Score: {candidate.mcq_result.percentage_correct}%")
            
        print(f"Psychometric Result: {'✅ Found' if candidate.psychometric_result else '❌ Missing'}")
        if candidate.psychometric_result:
             print(f"  - Extraversion: {candidate.psychometric_result.extraversion}")

        print(f"Text Assessment Result: {'✅ Found' if candidate.text_assessment_result else '❌ Missing'}")
        
        print(f"Existing Rationale: {'✅ Found' if candidate.rationale else '❌ Missing'}")
        if candidate.rationale:
            print("  - Rationale JSON:", candidate.rationale.rationale_json)

if __name__ == "__main__":
    try:
        inspect_db()
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
