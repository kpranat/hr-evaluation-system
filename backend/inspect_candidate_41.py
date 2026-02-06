
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import CandidateAuth, TextAssessmentResult, ProctorSession, ProctoringViolation, RecruiterAuth

def inspect_data():
    app = create_app()
    with app.app_context():
        print("🔍 Inspecting Candidate 41 (John Doe)...")
        candidate = CandidateAuth.query.get(41)
        if not candidate:
            print("❌ Candidate 41 not found.")
            return

        print(f"👤 Candidate: {candidate.name} ({candidate.email})")
        
        # 1. Soft Skills (TextAssessmentResult)
        text_res = TextAssessmentResult.query.filter_by(candidate_id=41).first()
        if text_res:
            print(f"📝 Text Result: Found. Grading: {json.dumps(text_res.grading_json)}")
        else:
            print("❌ Text Result: Not found.")

        # 2. Proctoring (ProctorSession & Violations)
        proctor_sess = ProctorSession.query.filter_by(candidate_id=41).all()
        print(f"🛡️  Proctor Sessions: {len(proctor_sess)}")
        for i, sess in enumerate(proctor_sess):
            print(f"  Session {i+1} [UUID: {sess.session_uuid}]: Violation Counts: {json.dumps(sess.violation_counts)[:100]}...")
            
            # Check related violations in table
            violation_rows = ProctoringViolation.query.filter_by(session_id=sess.session_uuid).all()
            print(f"    -> Linked Violation Rows in DB: {len(violation_rows)}")

        # 3. Recruiters (for login)
        print("\n🔑 Recruiters:")
        recruiters = RecruiterAuth.query.all()
        for r in recruiters:
            print(f"  - {r.email}")

if __name__ == "__main__":
    inspect_data()
