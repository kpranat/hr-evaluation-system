from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

#======================= candidate login ============================
class CandidateAuth(db.Model):
    __tablename__ = 'candidate_auth'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)  # Increased length for hashed password
    
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

