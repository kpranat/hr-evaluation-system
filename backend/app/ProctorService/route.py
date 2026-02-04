from flask import request, jsonify
from . import ProctorService
from ..models import ProctorSession, ProctorEvent, CandidateAuth
from ..extensions import db
from ..config import Config
import jwt
from datetime import datetime
import json

# ANSI color codes for console output
class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def log_proctor_event(event_type, session_id, user_id, details=None):
    """Log proctor events to console with color formatting."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    # Determine color based on severity
    if event_type in ['multiple_faces', 'no_face', 'phone_detected']:
        color = Colors.RED
        severity = 'CRITICAL'
    elif event_type in ['looking_away', 'tab_switch']:
        color = Colors.YELLOW
        severity = 'WARNING'
    else:
        color = Colors.CYAN
        severity = 'INFO'
    
    print(f"\n{color}{Colors.BOLD}" + "="*60 + f"{Colors.END}")
    print(f"{color}{Colors.BOLD}[PROCTOR {severity}] {timestamp}{Colors.END}")
    print(f"{color}  Session: {session_id} | User: {user_id}{Colors.END}")
    print(f"{color}  Event: {event_type.upper()}{Colors.END}")
    if details:
        print(f"{color}  Details: {details}{Colors.END}")
    print(f"{color}{Colors.BOLD}" + "="*60 + f"{Colors.END}\n")

def verify_candidate_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
        return payload.get('user_id')
    except:
        return None

@ProctorService.route('/session/start', methods=['POST'])
def start_session():
    user_id = verify_candidate_token()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.json
    assessment_id = data.get('assessment_id')
    
    session = ProctorSession(
        candidate_id=user_id,
        assessment_id=assessment_id,
        start_time=datetime.utcnow(),
        status='active'
    )
    db.session.add(session)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'session_id': session.id,
        'message': 'Proctoring session started'
    })

@ProctorService.route('/session/end', methods=['POST'])
def end_session():
    user_id = verify_candidate_token()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.json
    session_id = data.get('session_id')
    
    session = ProctorSession.query.get(session_id)
    if not session or session.candidate_id != user_id:
        return jsonify({'error': 'Invalid session'}), 404
        
    session.end_time = datetime.utcnow()
    session.status = 'completed'
    db.session.commit()
    
    return jsonify({'success': True})

@ProctorService.route('/log-event', methods=['POST'])
def log_event():
    user_id = verify_candidate_token()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.json
    session_id = data.get('session_id')
    event_type = data.get('event_type')
    details = data.get('details')
    
    # Optional: Verify session belongs to user
    
    # Log to console for visibility
    log_proctor_event(event_type, session_id, user_id, details)
    
    event = ProctorEvent(
        session_id=session_id,
        event_type=event_type,
        details=str(details) if details else None,
        timestamp=datetime.utcnow()
    )
    db.session.add(event)
    db.session.commit()
    
    return jsonify({'success': True})
@ProctorService.route('/analyze-frame', methods=['POST'])
def analyze_frame():
    user_id = verify_candidate_token()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.json
    session_id = data.get('session_id')
    image_data = data.get('image')
    
    if not image_data:
        return jsonify({'error': 'No image data provided'}), 400

    # Call AI Service
    from ..services.ai_service import analyze_frame_with_llama
    result = analyze_frame_with_llama(image_data)
    
    # Auto-log if suspicious behavior detected
    if result.get('multiple_faces') or result.get('looking_away') or result.get('phone_detected') or not result.get('face_detected'):
        # Log event internally
        event_type = 'suspicious_behavior'
        if result.get('multiple_faces'): event_type = 'multiple_faces'
        elif not result.get('face_detected'): event_type = 'no_face'
        elif result.get('looking_away'): event_type = 'looking_away'
        
        # Log to console for visibility
        log_proctor_event(event_type, session_id, user_id, result)
        
        event = ProctorEvent(
            session_id=session_id,
            event_type=event_type,
            details=json.dumps(result),
            severity='warning',
            timestamp=datetime.utcnow()
        )
        db.session.add(event)
        db.session.commit()
    
    return jsonify({
        'success': True,
        'analysis': result
    })

@ProctorService.route('/session/<int:session_id>/summary', methods=['GET'])
def get_session_summary(session_id):
    """
    Get complete proctoring data for a session.
    This endpoint is designed for the EVALUATION ENGINE to access candidate behavior data.
    """
    # TODO: Add recruiter/admin auth check for production
    
    session = ProctorSession.query.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    
    # Get all events for this session
    events = ProctorEvent.query.filter_by(session_id=session_id).order_by(ProctorEvent.timestamp).all()
    
    # Count violations by type
    violation_counts = {}
    for event in events:
        violation_counts[event.event_type] = violation_counts.get(event.event_type, 0) + 1
    
    # Calculate risk score (simple algorithm for now)
    risk_score = 0
    risk_score += violation_counts.get('no_face', 0) * 10
    risk_score += violation_counts.get('multiple_faces', 0) * 25
    risk_score += violation_counts.get('looking_away', 0) * 5
    risk_score += violation_counts.get('tab_switch', 0) * 15
    risk_score += violation_counts.get('phone_detected', 0) * 20
    risk_score = min(risk_score, 100)  # Cap at 100
    
    return jsonify({
        'success': True,
        'session': {
            'id': session.id,
            'candidate_id': session.candidate_id,
            'assessment_id': session.assessment_id,
            'start_time': session.start_time.isoformat() if session.start_time else None,
            'end_time': session.end_time.isoformat() if session.end_time else None,
            'status': session.status,
            'duration_minutes': round((session.end_time - session.start_time).total_seconds() / 60, 2) if session.end_time and session.start_time else None
        },
        'violations': {
            'total_count': len(events),
            'by_type': violation_counts
        },
        'risk_score': risk_score,
        'events': [
            {
                'id': e.id,
                'type': e.event_type,
                'severity': e.severity,
                'timestamp': e.timestamp.isoformat() if e.timestamp else None,
                'details': e.details
            } for e in events
        ]
    })

@ProctorService.route('/candidate/<int:candidate_id>/sessions', methods=['GET'])
def get_candidate_sessions(candidate_id):
    """
    Get all proctoring sessions for a candidate.
    Useful for evaluation engine to aggregate behavior across assessments.
    """
    sessions = ProctorSession.query.filter_by(candidate_id=candidate_id).order_by(ProctorSession.start_time.desc()).all()
    
    result = []
    for session in sessions:
        event_count = ProctorEvent.query.filter_by(session_id=session.id).count()
        result.append({
            'id': session.id,
            'assessment_id': session.assessment_id,
            'start_time': session.start_time.isoformat() if session.start_time else None,
            'end_time': session.end_time.isoformat() if session.end_time else None,
            'status': session.status,
            'total_violations': event_count
        })
    
    return jsonify({
        'success': True,
        'candidate_id': candidate_id,
        'sessions': result
    })
