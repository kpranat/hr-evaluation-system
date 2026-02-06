"""
Assessment Routes
Handles overall assessment logic and final submission
"""

from flask import request, jsonify, current_app
from . import Assessment
from ..auth_helpers import verify_candidate_token
from services.AI_rationale import process_ai_rationale

@Assessment.route('/finish', methods=['POST'])
def finish_assessment():
    """
    FINISH ASSESSMENT ENDPOINT
    
    Triggers the final AI rationale generation after all rounds are completed.
    
    Authentication: Required (JWT Bearer token - candidate only)
    
    Response:
        Success (200):
        {
            "success": true,
            "message": "Assessment completed and rationale generated.",
            "rationale": { ... }
        }
    """
    # Verify authentication
    candidate_id, error_response = verify_candidate_token()
    if error_response:
        return error_response
    
    print(f"\n🎓 Candidate {candidate_id} is finishing the assessment...")
    
    try:
        from ..models import CandidateAuth
        from ..extensions import db
        from datetime import datetime

        # Fetch candidate to update timestamps
        candidate = CandidateAuth.query.get(candidate_id)
        if candidate:
            now = datetime.now()
            # Update timestamps for completed sections to ensure valid sorting
            # This effectively "bumps" the candidate to the top of the dashboard
            if candidate.mcq_completed:
                candidate.mcq_completed_at = now
            if candidate.psychometric_completed:
                candidate.psychometric_completed_at = now
            if candidate.technical_completed:
                candidate.technical_completed_at = now
            if candidate.text_based_completed:
                candidate.text_based_completed_at = now
            if candidate.coding_completed:
                candidate.coding_completed_at = now
                
            db.session.commit()
            print(f"✅ Updated completion timestamps for Candidate {candidate_id}")
        
        # Trigger the AI Rationale Service
        # We pass the current_app._get_current_object() to ensure the service 
        # uses the same app context/config if needed (though the service handles context creation too)
        
        # Note: process_ai_rationale handles fetching data from DB for this candidate_id
        rationale_result = process_ai_rationale(candidate_id, app_instance=current_app._get_current_object())
        
        if not rationale_result:
            return jsonify({
                "success": False,
                "message": "Failed to generate rationale. Please contact support."
            }), 500

        return jsonify({
            "success": True,
            "message": "Assessment completed successfully. AI Rationale generated.",
            "rationale": rationale_result
        }), 200

    except Exception as e:
        print(f"❌ FINISH ASSESSMENT ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"An error occurred: {str(e)}"
        }), 500
