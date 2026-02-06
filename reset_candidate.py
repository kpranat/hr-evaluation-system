
import sys
import os
from datetime import datetime

# Add backend directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app import create_app, db
from app.models import CandidateAuth

if len(sys.argv) < 2:
    print("Usage: backend/venv/bin/python3 reset_candidate.py <email>")
    sys.exit(1)

email_to_reset = sys.argv[1]

app = create_app()

with app.app_context():
    candidate = CandidateAuth.query.filter_by(email=email_to_reset).first()
    
    if not candidate:
        print(f"❌ Candidate with email {email_to_reset} not found.")
        sys.exit(1)
    
    print(f"found candidate {candidate.id} ({candidate.email})")
    print(f"Current Status: Coding Completed={candidate.coding_completed}")
    
    # Reset flags
    candidate.mcq_completed = False
    candidate.psychometric_completed = False
    candidate.technical_completed = False
    candidate.text_based_completed = False
    candidate.coding_completed = False
    
    db.session.commit()
    print(f"✅ Successfully reset progress for {email_to_reset}. You can now login again.")
