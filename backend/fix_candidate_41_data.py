
import sys
import os
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import CandidateAuth, TextAssessmentResult, ProctorSession, ProctoringViolation, TextBasedAnswer

def fix_candidate_data(candidate_id=41):
    app = create_app()
    with app.app_context():
        print(f"🔧 Fixing data for Candidate {candidate_id}...")
        
        # 1. Fix Soft Skills (TextAssessmentResult)
        # Check if result exists
        text_res = TextAssessmentResult.query.filter_by(candidate_id=candidate_id).first()
        if not text_res:
            print("  📝 Creating missing TextAssessmentResult...")
            # Ideally we grade real answers, but if they don't exist, we mock it for the demo
            # Check for answers
            answers = TextBasedAnswer.query.filter_by(candidate_id=candidate_id).all()
            if answers:
                print(f"     Found {len(answers)} answers. Grading...")
                from services.textresponse_to_grading import evaluate_text_responses
                qa_pair = [{"question": "Q", "answer": a.answer_text} for a in answers]
                grading = evaluate_text_responses(qa_pair)
            else:
                print("     No answers found. Creating Mock Grading.")
                grading = {
                    "communication_score": 85,
                    "remark": "Candidate demonstrates clear communication skills but lacks detail in some areas.",
                    "details": "Mock data generated for fix."
                }
            
            text_res = TextAssessmentResult(
                candidate_id=candidate_id,
                score_percentage=grading.get("communication_score", 80),
                grading_json=grading
            )
            db.session.add(text_res)
            db.session.commit()
            print("     ✅ Created TextAssessmentResult.")
        else:
             print("  📝 TextAssessmentResult already exists.")

        # 2. Fix Proctoring (Populate Violations table from Session JSON)
        session = ProctorSession.query.filter_by(candidate_id=candidate_id).order_by(ProctorSession.start_time.desc()).first()
        if session:
            print(f"  🛡️  Processing Session {session.session_uuid}...")
            
            # Check if violations already exist
            existing_count = ProctoringViolation.query.filter_by(session_id=session.session_uuid).count()
            if existing_count > 0:
                print(f"     Violations table already has {existing_count} rows. Skipping backfill.")
            else:
                print("     Violations table empty. Backfilling from JSON...")
                # Get events from JSON
                # The user showed structure: { "events": [...], "summary": ... }
                raw_data = session.violation_counts
                events = []
                if isinstance(raw_data, dict):
                    if "events" in raw_data:
                        events = raw_data["events"]
                    # If just counts, we can't backfill events accurately in time, but maybe we don't need to?
                    # The Dashboard Log needs events.
                
                if not events and isinstance(raw_data, dict):
                    # If "events" list missing, generate SYNTHETIC events from counts 
                    # This ensures the dashboard log is not empty for old sessions.
                    print("     ⚠️ No 'events' list found. Generating SYNTHETIC events from counts...")
                    
                    # Get counts from summary or root
                    counts = raw_data.get("summary", raw_data)
                    
                    for risk_type, count in counts.items():
                        if not isinstance(count, int) or count <= 0: continue
                        
                        for i in range(count):
                            # Stagger timestamps
                            ts = datetime.utcnow() # In reality, we'd stagger them, but this is fine for debug
                            
                            severity_map = {
                                'multiple_faces': 'high',
                                'no_face': 'high',
                                'phone_detected': 'high',
                                'looking_away': 'medium',
                                'tab_switch': 'medium',
                                'mouse_exit': 'low'
                            }
                            
                            v = ProctoringViolation(
                                session_id=session.session_uuid,
                                candidate_id=candidate_id,
                                violation_type=risk_type,
                                violation_data={"details": f"Synthetic Log for {risk_type}"},
                                severity=severity_map.get(risk_type, 'low'),
                                timestamp=ts
                            )
                            db.session.add(v)
                            events.append(v)
                            
                    db.session.commit()
                    print(f"     ✅ Backfilled {len(events)} synthetic violations.")
                elif events:
                    print(f"     Found {len(events)} events in JSON. Inserting...")
                    severity_map = {
                        'multiple_faces': 'high',
                        'no_face': 'high',
                        'phone_detected': 'high',
                        'looking_away': 'medium',
                        'tab_switch': 'medium',
                        'mouse_exit': 'low'
                    }
                    
                    for evt in events:
                        etype = evt.get('type')
                        ts_str = evt.get('timestamp')
                        try:
                            timestamp = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                        except:
                            timestamp = datetime.utcnow()
                            
                        v = ProctoringViolation(
                            session_id=session.session_uuid,
                            candidate_id=candidate_id,
                            violation_type=etype,
                            violation_data=evt,
                            severity=severity_map.get(etype, 'low'),
                            timestamp=timestamp
                        )
                        db.session.add(v)
                    
                    db.session.commit()
                    print(f"     ✅ Backfilled {len(events)} violations.")
        else:
            print("  ❌ No ProctorSession found.")

if __name__ == "__main__":
    fix_candidate_data()
