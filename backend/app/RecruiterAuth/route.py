"""
RecruiterAuth Routes
Handles recruiter authentication operations
"""

from flask import request, jsonify
from . import RecruiterAuth
from ..models import RecruiterAuth as RecruiterAuthModel
from ..extensions import db
from ..config import Config
import jwt
from datetime import datetime, timedelta


@RecruiterAuth.route('/login', methods=['POST'])
def login():
    """
    RECRUITER LOGIN ENDPOINT
    
    Authenticates recruiter credentials and returns JWT token for subsequent requests.
    
    Authentication: Not required (public endpoint)
    
    Request:
        - Method: POST
        - Content-Type: application/json
        - Body: {
            "email": "recruiter@example.com",
            "password": "plain_text_password"
        }
        
    Response:
        Success (200):
        {
            "success": true,
            "message": "Login successful",
            "token": "JWT_TOKEN_STRING",
            "user": {
                "id": 1,
                "email": "recruiter@example.com"
            }
        }
        
        Failure (400/401):
        {
            "success": false,
            "message": "Error message"
        }
        
    Status Codes:
        - 200: Login successful
        - 400: Missing email or password
        - 401: Invalid credentials
        - 500: Server error
        
    Processing Logic:
        1. Validate request contains email and password
        2. Query database for recruiter by email
        3. Verify password using check_password() method
        4. Generate JWT token with recruiter details
        5. Return token and user info
        
    Token Details:
        - Algorithm: HS256
        - Expiration: Configured in Config.JWT_EXP_MINUTES
        - Payload includes: user_id, email, type='recruiter', exp
    """
    try:
        data = request.get_json()
        
        # Validate that email and password are provided
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        email = data.get('email')
        password = data.get('password')
        
        # Query database for recruiter by email
        recruiter = RecruiterAuthModel.query.filter_by(email=email).first()
        
        # Return error if recruiter not found
        if not recruiter:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Verify password using werkzeug's check_password_hash
        if not recruiter.check_password(password):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Generate JWT token with recruiter information
        token_payload = {
            'user_id': recruiter.id,
            'email': recruiter.email,
            'type': 'recruiter',
            'exp': datetime.utcnow() + timedelta(minutes=Config.JWT_EXP_MINUTES)
        }
        
        token = jwt.encode(token_payload, Config.JWT_SECRET, algorithm='HS256')
        
        # Return success response with token and user details
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': recruiter.to_dict()
        }), 200
        
    except Exception as e:
        import traceback
        print(f"\n❌ RECRUITER LOGIN ERROR: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500


@RecruiterAuth.route('/verify', methods=['GET'])
def verify_token():
    """
    TOKEN VERIFICATION ENDPOINT
    
    Verifies the validity of a JWT token and returns user information.
    Used to check if a recruiter session is still valid.
    
    Authentication: Required (JWT Bearer token)
    
    Request:
        - Method: GET
        - Headers: {
            "Authorization": "Bearer JWT_TOKEN_STRING"
        }
        
    Response:
        Success (200):
        {
            "valid": true,
            "user": {
                "id": 1,
                "email": "recruiter@example.com",
                "type": "recruiter"
            }
        }
        
        Failure (401):
        {
            "valid": false,
            "message": "Error message"
        }
        
    Status Codes:
        - 200: Token is valid
        - 401: Missing token, invalid token, expired token, or wrong token type
        - 500: Server error
        
    Processing Logic:
        1. Extract token from Authorization header
        2. Decode and verify token using JWT_SECRET
        3. Verify token type is 'recruiter'
        4. Return user information from token payload
        
    Token Validation:
        - Checks token signature
        - Checks token expiration
        - Verifies token type matches 'recruiter'
        
    Use Cases:
        - Session validation on app load
        - Protected route authentication
        - Token refresh validation
    """
    try:
        # Extract Authorization header
        auth_header = request.headers.get('Authorization')
        
        # Validate that token is present and properly formatted
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'valid': False,
                'message': 'No token provided'
            }), 401
        
        # Extract token from "Bearer TOKEN" format
        token = auth_header.split(' ')[1]
        
        try:
            # Decode and verify token
            payload = jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
            
            # Verify it's a recruiter token (not candidate or other type)
            if payload.get('type') != 'recruiter':
                return jsonify({
                    'valid': False,
                    'message': 'Invalid token type'
                }), 401
            
            # Return success with user information from token
            return jsonify({
                'valid': True,
                'user': {
                    'id': payload.get('user_id'),
                    'email': payload.get('email'),
                    'type': payload.get('type')
                }
            }), 200
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                'valid': False,
                'message': 'Token has expired'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'valid': False,
                'message': 'Invalid token'
            }), 401
            
    except Exception as e:
        import traceback
        print(f"\n❌ TOKEN VERIFICATION ERROR: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'valid': False,
            'message': f'An error occurred: {str(e)}'
        }), 500
