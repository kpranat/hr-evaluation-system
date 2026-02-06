
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import CandidateAuth, TextAssessmentResult, ProctorSession, MCQResult

def debug_dashboard_logic(candidate_id=41):
    app = create_app()
    with app.app_context():
        print(f"🕵️‍♂️ Debugging Dashboard Logic for Candidate {candidate_id}...")
        
        candidate = CandidateAuth.query.get(candidate_id)
        if not candidate:
            print("❌ Candidate not found.")
            return

        # 1. Technical Score (MCQ)
        mcq_result = MCQResult.query.filter_by(student_id=candidate.id).first()
        technical_score = mcq_result.percentage_correct if mcq_result else 0
        print(f"📊 Technical Score: {technical_score} (MCQ Found: {mcq_result is not None})")

        # 2. Soft Skills (TextAssessment)
        text_result = db.session.query(TextAssessmentResult).filter_by(candidate_id=candidate.id).first()
        soft_skill_score = 0
        if text_result:
            print(f"📝 TextResult Found. Grading JSON: {json.dumps(text_result.grading_json)}")
            if text_result.grading_json:
                 soft_skill_score = text_result.grading_json.get('communication_score', 0)
        else:
            print("❌ No TextAssessmentResult found.")
        print(f"📊 Soft Skill Score: {soft_skill_score}")

        # 3. Fairplay (Proctor)
        sessions = ProctorSession.query.filter_by(candidate_id=candidate.id).order_by(ProctorSession.start_time.desc()).all()
        print(f"🛡️  Found {len(sessions)} ProctorSessions.")
        
        for i, session in enumerate(sessions):
            print(f"  Session {i+1} [UUID: {session.session_uuid}]:")
            print(f"    Raw Violation Counts: {json.dumps(session.violation_counts)}")
            
            # Logic Test
            temp_score = 100
            if session.violation_counts:
                raw_data = session.violation_counts
                if "summary" in raw_data:
                    counts = raw_data["summary"]
                else:
                    counts = raw_data
                
                deductions = 0
                deductions += (counts.get('phone_detected', 0) * 15)
                deductions += (counts.get('multiple_faces', 0) * 15)
                deductions += (counts.get('no_face', 0) * 15)
                deductions += (counts.get('tab_switch', 0) * 8)
                deductions += (counts.get('looking_away', 0) * 8)
                print(f"    Deductions for this session: {deductions}")
            
        if sessions:
             print(f"  -> Route uses Session 1 (Latest).")
             # Re-calc for latest to show what route sees
             session = sessions[0]
             fairplay_score = 100
             if session.violation_counts:
                raw_data = session.violation_counts
                if "summary" in raw_data:
                    counts = raw_data["summary"]
                else:
                    counts = raw_data
                deductions = (counts.get('phone_detected', 0) * 15) + \
                             (counts.get('multiple_faces', 0) * 15) + \
                             (counts.get('no_face', 0) * 15) + \
                             (counts.get('tab_switch', 0) * 8) + \
                             (counts.get('looking_away', 0) * 8)
                fairplay_score -= deductions
        else:
            print("❌ No ProctorSession found.")
            fairplay_score = 100
        print(f"📊 Fairplay Score: {fairplay_score}")

if __name__ == "__main__":
    debug_dashboard_logic()
