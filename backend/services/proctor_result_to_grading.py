
import json
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import ProctorSession, ProctoringViolation

def process_proctor_grading(candidate_id, app_instance=None):
    """
    Analyzes proctoring violations and categorizes malpractice severity.
    Updates ProctorSession.grading_json.
    """
    app = app_instance if app_instance else create_app()
    context = app.app_context() if not app_instance else None
    
    if context:
        context.push()
        
    try:
        print(f"🛡️  Processing Proctor Grading for Candidate {candidate_id}...")
        
        # 1. Get latest active or completed session
        session = ProctorSession.query.filter_by(candidate_id=candidate_id).order_by(ProctorSession.start_time.desc()).first()
        
        if not session:
            print(f"⚠️ No proctor session found for candidate {candidate_id}.")
            return {"severity": "None", "remark": "No session recorded."}
            
        if not session.violation_counts:
             print("⚠️ No violation counts found in session.")
             # It might be empty dict, which is fine, just means clean session
             counts = {
                "multiple_faces": 0,
                "no_face": 0,
                "phone_detected": 0,
                "looking_away": 0,
                "tab_switch": 0
             }
        else:
             # Handle nested summary structure if present (as per user's provided JSON)
             raw_data = session.violation_counts
             if "summary" in raw_data:
                 raw_counts = raw_data["summary"]
             else:
                 raw_counts = raw_data

             # Ensure defaults if keys missing
             counts = {
                "multiple_faces": raw_counts.get("multiple_faces", 0),
                "no_face": raw_counts.get("no_face", 0),
                "phone_detected": raw_counts.get("phone_detected", 0),
                "looking_away": raw_counts.get("looking_away", 0),
                "tab_switch": raw_counts.get("tab_switch", 0)
             }
             
        # 4. Apply Logic
        # Severe: Any phone, multiple faces > 2, or no face > 5
        # Moderate: Tab switch > 3, Looking away > 10
        # Light: Occasional looking away
        
        severity = "Clean"
        remark = "Candidate adhered to fair play rules."
        
        if counts["phone_detected"] > 0:
            severity = "Severe"
            remark = "Phone detected during assessment. Immediate disqualification recommended."
        elif counts["multiple_faces"] > 2:
            severity = "Severe"
            remark = "Multiple faces detected frequently. Potential collaboration."
        elif counts["no_face"] > 10: # Increased threshold as no_face can be flaky light
            severity = "Severe" 
            remark = "Candidate frequently left the frame or camera was obscured."
        elif counts["tab_switch"] > 4:
            severity = "Moderate"
            remark = "Frequent tab switching detected. Potential research or copy-pasting."
        elif counts["looking_away"] > 15:
            severity = "Moderate"
            remark = "Candidate frequently looking away from screen."
        elif sum(counts.values()) > 0:
            severity = "Light"
            remark = "Minor behavioral flags detected but likely benign."
            
        grading_json = {
            "severity": severity,
            "remark": remark,
            "violation_summary": counts
        }
        
        # 5. Store in DB
        session.grading_json = grading_json
        db.session.commit()
        
        print(f"✅ Proctor Grading Saved: {severity}")
        return grading_json

    except Exception as e:
        print(f"❌ Error in process_proctor_grading: {e}")
        return {"error": str(e)}
    finally:
        if context:
            context.pop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 proctor_result_to_grading.py <candidate_id>")
    else:
        process_proctor_grading(int(sys.argv[1]))
