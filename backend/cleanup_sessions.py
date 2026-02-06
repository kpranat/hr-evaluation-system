
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import ProctorSession

def cleanup_empty_sessions(candidate_id=41):
    app = create_app()
    with app.app_context():
        print(f"🧹 Cleaning up empty sessions for Candidate {candidate_id}...")
        
        sessions = ProctorSession.query.filter_by(candidate_id=candidate_id).order_by(ProctorSession.start_time.desc()).all()
        print(f"found {len(sessions)} sessions.")
        
        deleted_count = 0
        for s in sessions:
            # Check if empty or near empty
            is_empty = False
            if not s.violation_counts:
                is_empty = True
            else:
                # Check looking deeper
                data = s.violation_counts
                summary = data.get("summary", data)
                total = sum(summary.values()) if isinstance(summary, dict) else 0
                if total == 0:
                    is_empty = True
            
            if is_empty:
                print(f"  🗑️ Deleting Empty Session {s.session_uuid}...")
                db.session.delete(s)
                deleted_count += 1
            else:
                print(f"  ✅ Keeping Session {s.session_uuid} (Total Violations: {total if 'total' in locals() else 'Unknown'})")
        
        if deleted_count > 0:
            db.session.commit()
            print(f"✨ Deleted {deleted_count} empty sessions. Dashboard should now pick the latest valid one.")
        else:
            print("No empty sessions found to delete.")

if __name__ == "__main__":
    cleanup_empty_sessions()
