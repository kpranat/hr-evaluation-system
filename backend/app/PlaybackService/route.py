from flask import request, jsonify
from . import PlaybackService
from ..models import CodePlayback, ProctorSession
from ..extensions import db
from ..config import Config
import jwt
import json
from datetime import datetime

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

@PlaybackService.route('/record', methods=['POST'])
def record_playback():
    user_id = verify_candidate_token()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.json
    session_id = data.get('session_id')
    question_id = data.get('question_id')
    new_events = data.get('events', []) # List of events
    
    if not session_id or not question_id:
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if a log already exists for this session+question
    log = CodePlayback.query.filter_by(session_id=session_id, question_id=question_id).first()
    
    if log:
        # Append to existing events
        # Note: In production, might want to store as separate rows or append optimized delta
        # For MVP, we load, append, save. 
        try:
            current_events = json.loads(log.events) if log.events else []
            current_events.extend(new_events)
            log.events = json.dumps(current_events)
        except:
            log.events = json.dumps(new_events)
    else:
        log = CodePlayback(
            session_id=session_id,
            question_id=question_id,
            events=json.dumps(new_events)
        )
        db.session.add(log)
    
    db.session.commit()
    return jsonify({'success': True})

@PlaybackService.route('/session/<int:session_id>/question/<int:question_id>', methods=['GET'])
def get_playback(session_id, question_id):
    # TODO: Add recruiter auth check here
    
    log = CodePlayback.query.filter_by(session_id=session_id, question_id=question_id).first()
    
    if not log:
        return jsonify({'success': False, 'message': 'No recording found'}), 404
        
    return jsonify({
        'success': True,
        'events': json.loads(log.events) if log.events else []
    })
