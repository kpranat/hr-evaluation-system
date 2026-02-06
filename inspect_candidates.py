
import sys
import os
from datetime import datetime

# Add backend directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app import create_app, db
from app.models import CandidateAuth

app = create_app()

with app.app_context():
    print(f"Checking candidates in database...")
    candidates = CandidateAuth.query.all()
    
    if not candidates:
        print("No candidates found in database.")
    
    for c in candidates:
        print(f"ID: {c.id} | Email: {c.email}")
        print(f"  - MCQ Completed: {c.mcq_completed}")
        print(f"  - Psychometric Completed: {c.psychometric_completed}")
        print(f"  - Technical Completed: {c.technical_completed}")
        print(f"  - Text Based Completed: {c.text_based_completed}")
        print(f"  - Coding Completed: {c.coding_completed}")
        print(f"  - Resume URL: {c.resume_url}")
        print("-" * 40)
