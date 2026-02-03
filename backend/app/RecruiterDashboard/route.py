"""
RecruiterDashboard Routes
Handles all recruiter dashboard operations
"""

from flask import request, jsonify
from . import RecruiterDashboard
from ..models import CandidateAuth
from ..extensions import db
from ..config import Config
import jwt
import pandas as pd
import io


def verify_recruiter_token(request):
    """
    Helper function to verify recruiter JWT token
    
    Args:
        request: Flask request object containing Authorization header
        
    Returns:
        tuple: (success: bool, payload: dict or error_message: str, status_code: int)
    """
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return False, 'Authentication required', 401
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
        
        # Verify it's a recruiter token
        if payload.get('type') != 'recruiter':
            return False, 'Unauthorized: Recruiter access required', 403
            
        return True, payload, 200
        
    except jwt.ExpiredSignatureError:
        return False, 'Token has expired', 401
    except jwt.InvalidTokenError:
        return False, 'Invalid token', 401


@RecruiterDashboard.route('/candidates/upload', methods=['POST'])
def upload_candidates():
    """
    BULK CANDIDATE UPLOAD ENDPOINT
    
    Handles bulk upload of candidates from CSV or Excel files.
    Automatically hashes passwords before storing in database.
    
    Authentication: Required (JWT Bearer token - recruiter only)
    
    Request:
        - Method: POST
        - Content-Type: multipart/form-data
        - Field: 'file' (CSV/Excel file)
        - File must contain columns: 'email', 'password'
        
    Supported file formats:
        - CSV (.csv)
        - Excel (.xlsx, .xls)
        
    File constraints:
        - Maximum size: 10MB
        - Required columns: email, password
        
    Response:
        {
            "success": true/false,
            "message": "Status message",
            "results": {
                "total": <number of rows processed>,
                "created": <number of new candidates created>,
                "updated": <number of existing candidates updated>,
                "skipped": <number of rows skipped due to errors>,
                "errors": [<list of error messages>]
            }
        }
        
    Status Codes:
        - 200: Upload successful (even with partial errors)
        - 400: Bad request (missing file, invalid format, missing columns)
        - 401: Unauthorized (missing or invalid token)
        - 403: Forbidden (not a recruiter token)
        - 500: Server error (database error)
        
    Processing Logic:
        - For each row in the file:
            - If email exists: Update password (hashed)
            - If email doesn't exist: Create new candidate (password hashed)
            - If email/password missing: Skip row and log error
            
    Security:
        - Passwords are hashed using werkzeug.security.generate_password_hash()
        - Uses pbkdf2:sha256 algorithm
        - No plain text passwords are stored
    """
    try:
        # Verify recruiter authentication
        is_valid, payload_or_error, status_code = verify_recruiter_token(request)
        
        if not is_valid:
            return jsonify({
                'success': False,
                'message': payload_or_error
            }), status_code
        
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        # Check if a file was actually selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            }), 400
        
        # Validate file extension
        allowed_extensions = {'.csv', '.xlsx', '.xls'}
        file_ext = '.' + file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_ext not in allowed_extensions:
            return jsonify({
                'success': False,
                'message': f'Invalid file type. Allowed types: {", ".join(allowed_extensions)}'
            }), 400
        
        # Read file into pandas dataframe
        try:
            if file_ext == '.csv':
                df = pd.read_csv(io.BytesIO(file.read()))
            else:  # .xlsx or .xls
                df = pd.read_excel(io.BytesIO(file.read()))
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error reading file: {str(e)}'
            }), 400
        
        # Validate that required columns exist
        required_columns = ['email', 'password']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                'success': False,
                'message': f'Missing required columns: {", ".join(missing_columns)}'
            }), 400
        
        # Initialize results tracking
        results = {
            'total': len(df),
            'created': 0,
            'updated': 0,
            'skipped': 0,
            'errors': []
        }
        
        # Process each candidate row
        for index, row in df.iterrows():
            try:
                email = str(row['email']).strip()
                password = str(row['password']).strip()
                
                # Validate email is present
                if not email or email == 'nan':
                    results['skipped'] += 1
                    results['errors'].append(f"Row {index + 2}: Missing email")
                    continue
                
                # Validate password is present
                if not password or password == 'nan':
                    results['skipped'] += 1
                    results['errors'].append(f"Row {index + 2}: Missing password")
                    continue
                
                # Check if candidate already exists
                existing_candidate = CandidateAuth.query.filter_by(email=email).first()
                
                if existing_candidate:
                    # Update existing candidate's password (will be hashed)
                    existing_candidate.set_password(password)
                    results['updated'] += 1
                else:
                    # Create new candidate with hashed password
                    new_candidate = CandidateAuth(email=email)
                    new_candidate.set_password(password)  # Automatically hashes the password
                    db.session.add(new_candidate)
                    results['created'] += 1
                
            except Exception as e:
                results['skipped'] += 1
                results['errors'].append(f"Row {index + 2}: {str(e)}")
        
        # Commit all changes to database
        try:
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Successfully processed {results["total"]} candidates',
                'results': results
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Database error: {str(e)}',
                'results': results
            }), 500
            
    except Exception as e:
        import traceback
        print(f"\n❌ BULK UPLOAD ERROR: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500
