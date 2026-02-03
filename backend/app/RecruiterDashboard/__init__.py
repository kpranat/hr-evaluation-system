"""
RecruiterDashboard Blueprint
Handles all recruiter dashboard operations including:
- Bulk candidate management
- Candidate listing and details
- Analytics and reporting
"""

from flask import Blueprint

RecruiterDashboard = Blueprint('recruiter_dashboard', __name__)

from . import route
