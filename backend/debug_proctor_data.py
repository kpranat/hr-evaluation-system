
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import ProctorSession, ProctoringViolation, CandidateAuth

def debug_proctor_data():
    app = create_app()
    with app.app_context():
        print("🔍 Debugging Proctor Data...")
        
        # 1. Check Sessions
        sessions = ProctorSession.query.all()
        print(f"Found {len(sessions)} ProctorSessions.")
        for s in sessions:
            print(f"  Session [ID: {s.id}] UUID: {s.session_uuid} | Candidate: {s.candidate_id} | Grading: {s.grading_json}")
            
        # 2. Check Violations
        violations = ProctoringViolation.query.all()
        print(f"\nFound {len(violations)} ProctoringViolations.")
        for v in violations:
            print(f"  Violation [ID: {v.id}] SessionID: {v.session_id} | Type: {v.violation_type}")

        # 3. Check Connectivity
        print("\nChecking connectivity...")
        for s in sessions:
            related_violations = ProctoringViolation.query.filter_by(session_id=s.session_uuid).count()
            print(f"  Session {s.session_uuid} has {related_violations} violations linked via UUID.")
            # Check if any linked via ID
            related_via_id = ProctoringViolation.query.filter_by(session_id=str(s.id)).count()
            if related_via_id > 0:
                 print(f"  ⚠️ Session {s.session_uuid} has {related_via_id} violations linked via Integer ID!")

if __name__ == "__main__":
    debug_proctor_data()
