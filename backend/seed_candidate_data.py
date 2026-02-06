
import os
import sys
from datetime import datetime

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import CandidateAuth, MCQResult, PsychometricResult, TextAssessmentResult, CandidateRationale

def seed_data(candidate_id=1):
    app = create_app()
    with app.app_context():
        print(f"🌱 Seeding data for Candidate {candidate_id}...")
        
        candidate = CandidateAuth.query.get(candidate_id)
        if not candidate:
            print("❌ Candidate not found. Creating test candidate...")
            candidate = CandidateAuth(
                email="test_seed@example.com", 
                password="hashed_password_placeholder"
            )
            db.session.add(candidate)
            db.session.commit()
            candidate_id = candidate.id
            print(f"✅ Created Candidate {candidate_id}")
            
        # 1. Update Resume Data
        candidate.resume_url = "https://example.com/resume.pdf"
        candidate.resume_filename = "resume.pdf"
        candidate.resume_uploaded_at = datetime.utcnow()
        candidate.resume_data = {
            "skills": ["Python", "Flask", "React", "SQL"],
            "experience": ["Senior Developer at Tech Co (3 years)"],
            "education": ["BS Computer Science"],
            "summary": "Experienced full stack developer."
        }
        
        # 2. Update Completion Flags & Timestamps
        now = datetime.utcnow()
        candidate.mcq_completed = True
        candidate.mcq_completed_at = now
        candidate.psychometric_completed = True
        candidate.psychometric_completed_at = now
        candidate.technical_completed = True
        candidate.technical_completed_at = now
        candidate.text_based_completed = True
        candidate.text_based_completed_at = now
        
        # 3. Create/Update MCQ Result
        mcq = MCQResult.query.filter_by(student_id=candidate_id).first()
        if not mcq:
            mcq = MCQResult(student_id=candidate_id)
            db.session.add(mcq)
            
        mcq.correct_answers = 8
        mcq.wrong_answers = 2
        mcq.percentage_correct = 80.0
        mcq.grading_json = {"feedback": "Strong technical knowledge shown."}
        
        # 4. Create/Update Psychometric Result
        psy = PsychometricResult.query.filter_by(student_id=candidate_id).first()
        if not psy:
            psy = PsychometricResult(student_id=candidate_id)
            db.session.add(psy)
            
        psy.extraversion = 40.5
        psy.agreeableness = 35.0
        psy.conscientiousness = 45.0
        psy.emotional_stability = 42.0
        psy.intellect_imagination = 38.0
        psy.test_completed = True
        
        # 5. Create/Update Text Assessment Result
        txt = TextAssessmentResult.query.filter_by(candidate_id=candidate_id).first()
        if not txt:
            txt = TextAssessmentResult(candidate_id=candidate_id)
            db.session.add(txt)
            
        txt.grading_json = {
            "grade": "Good",
            "communication_score": 85,
            "remarks": "Candidate clearly articulated their thoughts and showed good problem solving."
        }
        
        db.session.commit()
        print("✅ Data seeded successfully!")
        
if __name__ == "__main__":
    seed_data()
