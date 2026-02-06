
import json
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import CodingSubmission, CodingAssessmentResult, CodingProblem

def process_coding_grading(candidate_id, app_instance=None):
    """
    Aggregates coding submissions for a candidate, calculates overall score,
    and stores a simplified summary in CodingAssessmentResult.
    """
    app = app_instance if app_instance else create_app()
    context = app.app_context() if not app_instance else None
    
    if context:
        context.push()
        
    try:
        print(f"👨‍💻 Processing Coding Grading for Candidate {candidate_id}...")
        
        # 1. Get all submissions for candidate
        submissions = CodingSubmission.query.filter_by(candidate_id=candidate_id).all()
        
        if not submissions:
            print(f"⚠️ No coding submissions found for candidate {candidate_id}.")
            return {
                "score_percentage": 0,
                "summary": "No code submitted."
            }

        # 2. Aggregate best submission per problem
        # Map: problem_id -> best_submission (highest score_percentage)
        best_submissions = {}
        for sub in submissions:
            pid = sub.problem_id
            if pid not in best_submissions:
                best_submissions[pid] = sub
            else:
                if sub.score_percentage > best_submissions[pid].score_percentage:
                    best_submissions[pid] = sub
                    
        # 3. Calculate metrics
        total_problems_attempted = len(best_submissions)
        # We assume total problems in the round is usually fixed, e.g. 3. 
        # But let's base it on what they attempted or maybe fetch config?
        # For simplicity, let's treat "100% on attempted" as the grade for now, 
        # OR better: Assume 3 problems (default config)
        total_problems_in_round = 3 
        
        total_score_sum = sum(sub.score_percentage for sub in best_submissions.values())
        overall_percentage = total_score_sum / total_problems_in_round
        overall_percentage = min(overall_percentage, 100.0) # Cap at 100
        
        # 4. Create Simplified JSON Summary
        passed_fully = sum(1 for sub in best_submissions.values() if sub.score_percentage == 100)
        
        details = []
        for pid, sub in best_submissions.items():
            problem = CodingProblem.query.filter_by(problem_id=pid).first()
            title = problem.title if problem else f"Problem {pid}"
            details.append({
                "problem": title,
                "status": sub.status,
                "score": sub.score_percentage,
                "efficiency": {
                    "runtime": f"{sub.runtime}ms" if sub.runtime else "N/A",
                    "memory": f"{sub.memory_usage}KB" if sub.memory_usage else "N/A"
                }
            })
            
        grading_json = {
            "summary": f"Solved {passed_fully}/{total_problems_in_round} problems fully.",
            "problems_attempted": total_problems_attempted,
            "details": details
        }
        
        # 5. Store in DB
        result_record = CodingAssessmentResult.query.filter_by(candidate_id=candidate_id).first()
        if not result_record:
            result_record = CodingAssessmentResult(candidate_id=candidate_id)
            db.session.add(result_record)
            
        result_record.score_percentage = round(overall_percentage, 2)
        result_record.grading_json = grading_json
        db.session.commit()
        
        print(f"✅ Coding Grading Saved: {overall_percentage}%")
        return grading_json
        
    except Exception as e:
        print(f"❌ Error in process_coding_grading: {e}")
        return {"error": str(e)}
    finally:
        if context:
            context.pop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 coding_result_to_grading.py <candidate_id>")
    else:
        process_coding_grading(int(sys.argv[1]))
