
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import ProctorSession, ProctoringViolation, CandidateAuth, CodingAssessmentResult, TextAssessmentResult

def debug_data():
    app = create_app()
    with app.app_context():
        print("🔍 Debugging All Data...")
        
        # 1. Proctor
        print(f"\n--- PROCTOR DATA ---")
        sessions = ProctorSession.query.all()
        print(f"Found {len(sessions)} ProctorSessions.")
        for s in sessions:
            print(f"  Session [ID: {s.id}] UUID: {s.session_uuid} | Candidate: {s.candidate_id} | Grading: {json.dumps(s.grading_json) if s.grading_json else 'None'}")
            if s.violation_counts:
                 print(f"  Violation Counts Raw: {json.dumps(s.violation_counts)[:100]}...") # Print first 100 chars
                 
        violations = ProctoringViolation.query.all()
        print(f"Found {len(violations)} ProctoringViolations.")

        # 2. Coding
        print(f"\n--- CODING DATA ---")
        coding_results = CodingAssessmentResult.query.all()
        print(f"Found {len(coding_results)} CodingAssessmentResults.")
        for c in coding_results:
             print(f"  Coding [Candidate: {c.candidate_id}] Score: {c.score_percentage}% | Grading: {json.dumps(c.grading_json) if c.grading_json else 'None'}")
             
        # 3. Text
        print(f"\n--- TEXT DATA ---")
        text_results = TextAssessmentResult.query.all()
        print(f"Found {len(text_results)} TextAssessmentResults.")
        for t in text_results:
             print(f"  Text [Candidate: {t.candidate_id}] Grading: {json.dumps(t.grading_json) if t.grading_json else 'None'}")

if __name__ == "__main__":
    debug_data()
