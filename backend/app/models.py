from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

#======================= candidate login ============================
class CandidateAuth(db.Model):
    __tablename__ = 'candidate_auth'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)  # Increased length for hashed password
    resume_url = db.Column(db.String(500), nullable=True)  # Supabase storage URL
    resume_filename = db.Column(db.String(255), nullable=True)  # Original filename
    resume_uploaded_at = db.Column(db.DateTime, nullable=True)  # Upload timestamp
    
    # Assessment round completion tracking
    mcq_completed = db.Column(db.Boolean, default=False, nullable=False)
    mcq_completed_at = db.Column(db.DateTime, nullable=True)
    psychometric_completed = db.Column(db.Boolean, default=False, nullable=False)
    psychometric_completed_at = db.Column(db.DateTime, nullable=True)
    technical_completed = db.Column(db.Boolean, default=False, nullable=False)
    technical_completed_at = db.Column(db.DateTime, nullable=True)
    
    def set_password(self, password):
        """Hash and set the password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'email': self.email,
            'resume_url': self.resume_url,
            'resume_filename': self.resume_filename,
            'resume_uploaded_at': self.resume_uploaded_at.isoformat() if self.resume_uploaded_at else None,
            'mcq_completed': self.mcq_completed,
            'mcq_completed_at': self.mcq_completed_at.isoformat() if self.mcq_completed_at else None,
            'psychometric_completed': self.psychometric_completed,
            'psychometric_completed_at': self.psychometric_completed_at.isoformat() if self.psychometric_completed_at else None,
            'technical_completed': self.technical_completed,
            'technical_completed_at': self.technical_completed_at.isoformat() if self.technical_completed_at else None
        }

#====================== recruiter login ============================
class RecruiterAuth(db.Model):
    __tablename__ = 'recruiter_auth'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    
    def set_password(self, password):
        """Hash and set the password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'email': self.email
        }

#====================== MCQ Questions ============================
class MCQQuestion(db.Model):
    __tablename__ = 'mcq_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, unique=True, nullable=False)  # Unique question identifier
    question = db.Column(db.Text, nullable=False)  # Question text
    option1 = db.Column(db.String(500), nullable=False)  # Option 1
    option2 = db.Column(db.String(500), nullable=False)  # Option 2
    option3 = db.Column(db.String(500), nullable=False)  # Option 3
    option4 = db.Column(db.String(500), nullable=False)  # Option 4
    correct_answer = db.Column(db.Integer, nullable=False)  # Correct option number (1, 2, 3, or 4)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self, include_answer=False):
        """Convert to dictionary for JSON serialization"""
        data = {
            'id': self.id,
            'question_id': self.question_id,
            'question': self.question,
            'options': [
                {'id': 1, 'text': self.option1},
                {'id': 2, 'text': self.option2},
                {'id': 3, 'text': self.option3},
                {'id': 4, 'text': self.option4}
            ]
        }
        if include_answer:
            data['correct_answer'] = self.correct_answer
        return data

#====================== MCQ Results ============================
class MCQResult(db.Model):
    __tablename__ = 'mcq_results'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('candidate_auth.id'), nullable=False, unique=True)
    correct_answers = db.Column(db.Integer, default=0, nullable=False)
    wrong_answers = db.Column(db.Integer, default=0, nullable=False)
    percentage_correct = db.Column(db.Float, default=0.0, nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationship to candidate
    candidate = db.relationship('CandidateAuth', backref=db.backref('mcq_result', uselist=False))
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'correct_answers': self.correct_answers,
            'wrong_answers': self.wrong_answers,
            'percentage_correct': self.percentage_correct,
            'total_answered': self.correct_answers + self.wrong_answers,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

