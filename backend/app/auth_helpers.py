"""
Authentication Helper Functions
Centralized JWT token verification for candidate and recruiter routes
"""

from flask import request, jsonify
from .config import Config
import jwt


def verify_candidate_token():
    """
    Verify candidate JWT token from Authorization header
    
    Returns:
        tuple: (candidate_id: int, error_response: tuple or None)
        - If valid: (candidate_id, None)
        - If invalid: (None, (error_dict, status_code))
    
    Usage:
        candidate_id, error = verify_candidate_token()
        if error:
            return error
        # Continue with authenticated candidate_id
    """
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, (jsonify({
            'success': False,
            'message': 'Authentication required. Please provide Bearer token.'
        }), 401)
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
        
        # Verify it's a candidate token
        if payload.get('type') != 'candidate':
            return None, (jsonify({
                'success': False,
                'message': 'Unauthorized: Candidate access required'
            }), 403)
        
        candidate_id = payload.get('user_id')
        if not candidate_id:
            return None, (jsonify({
                'success': False,
                'message': 'Invalid token: Missing user_id'
            }), 401)
        
        return candidate_id, None
        
    except jwt.ExpiredSignatureError:
        return None, (jsonify({
            'success': False,
            'message': 'Token has expired. Please login again.'
        }), 401)
    except jwt.InvalidTokenError as e:
        return None, (jsonify({
            'success': False,
            'message': f'Invalid token: {str(e)}'
        }), 401)
    except Exception as e:
        return None, (jsonify({
            'success': False,
            'message': f'Authentication error: {str(e)}'
        }), 500)


def verify_recruiter_token():
    """
    Verify recruiter JWT token from Authorization header
    
    Returns:
        tuple: (recruiter_id: int, error_response: tuple or None)
        - If valid: (recruiter_id, None)
        - If invalid: (None, (error_dict, status_code))
    
    Usage:
        recruiter_id, error = verify_recruiter_token()
        if error:
            return error
        # Continue with authenticated recruiter_id
    """
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        print(f"⚠ AUTH: No Bearer token in request. Header: {auth_header}")
        return None, (jsonify({
            'success': False,
            'message': 'Authentication required. Please provide Bearer token.'
        }), 401)
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
        
        # Debug: Print token payload
        print(f"🔍 AUTH: Token payload: user_id={payload.get('user_id')}, type={payload.get('type')}, email={payload.get('email')}")
        
        # Verify it's a recruiter token
        if payload.get('type') != 'recruiter':
            print(f"❌ AUTH: Token type mismatch. Expected 'recruiter', got '{payload.get('type')}'")
            return None, (jsonify({
                'success': False,
                'message': 'Unauthorized: Recruiter access required'
            }), 403)
        
        recruiter_id = payload.get('user_id')
        if not recruiter_id:
            return None, (jsonify({
                'success': False,
                'message': 'Invalid token: Missing user_id'
            }), 401)
        
        print(f"✓ AUTH: Recruiter authenticated - ID: {recruiter_id}")
        return recruiter_id, None
        
    except jwt.ExpiredSignatureError:
        print(f"⚠ AUTH: Token expired")
        return None, (jsonify({
            'success': False,
            'message': 'Token has expired. Please login again.'
        }), 401)
    except jwt.InvalidTokenError as e:
        print(f"❌ AUTH: Invalid token - {str(e)}")
        return None, (jsonify({
            'success': False,
            'message': f'Invalid token: {str(e)}'
        }), 401)
    except Exception as e:
        print(f"❌ AUTH: Unexpected error - {str(e)}")
        return None, (jsonify({
            'success': False,
            'message': f'Authentication error: {str(e)}'
        }), 500)


def get_token_payload():
    """
    Get full JWT token payload without user type validation
    Useful for endpoints that accept multiple user types
    
    Returns:
        tuple: (payload: dict, error_response: tuple or None)
        - If valid: (payload_dict, None)
        - If invalid: (None, (error_dict, status_code))
    """
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, (jsonify({
            'success': False,
            'message': 'Authentication required. Please provide Bearer token.'
        }), 401)
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
        return payload, None
        
    except jwt.ExpiredSignatureError:
        return None, (jsonify({
            'success': False,
            'message': 'Token has expired. Please login again.'
        }), 401)
    except jwt.InvalidTokenError as e:
        return None, (jsonify({
            'success': False,
            'message': f'Invalid token: {str(e)}'
        }), 401)
    except Exception as e:
        return None, (jsonify({
            'success': False,
            'message': f'Authentication error: {str(e)}'
        }), 500)
